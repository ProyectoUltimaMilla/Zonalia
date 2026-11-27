"""Generador de datos sintéticos de Zonalia (#15).

Crea 100 mil paquetes ficticios con su destinatario, manifiestos diarios en CSV y JSON,
rutas, asignaciones, entregas y el historial de estados, y los carga a PostgreSQL con COPY.
Todo sale de Faker con semilla fija: la misma semilla da siempre los mismos datos.
Ningún dato es real. Las colonias y zonas sí son las del catálogo (#9), que es público.

Uso, desde servicios/ con el entorno activado:
    python -m zonalia.generador                    genera los archivos en servicios/salida/
    python -m zonalia.generador --cargar           además los carga a la base (vacía)
    python -m zonalia.generador --cargar --reiniciar   vacía las tablas antes de cargar
"""

import argparse
import csv
import json
import math
import os
import random
import secrets
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import date, datetime, time, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

from faker import Faker

RAIZ = Path(__file__).resolve().parents[4]
CATALOGOS = RAIZ / "db" / "catalogos"
SALIDA = RAIZ / "servicios" / "salida"

ZONA_HORARIA = ZoneInfo("America/Mexico_City")
PRIMER_DIA = date(2026, 6, 1)
PAQUETES_POR_DIA = (600, 800)  # el centro recibe unos 700 al día
CAPACIDAD = 60  # repartidor.capacidad_diaria por omisión
CARGA_OBJETIVO = 0.75  # cada repartidor lleva en promedio el 75 % de su capacidad
PROBABILIDAD_FALLO = 0.12
MOTIVOS_FALLO = [
    "Nadie en el domicilio",
    "Dirección incompleta",
    "Destinatario rechazó el paquete",
    "Zona de difícil acceso",
]
REFERENCIAS = [
    "Portón negro",
    "Casa de dos pisos",
    "Frente a la tienda",
    "Junto al parque",
    "Departamento interior",
    "",
]
CENTRO_CIUDAD = (21.8818, -102.2916)


@dataclass
class Datos:
    """Todas las filas generadas, tabla por tabla, en el orden en que se cargan."""

    zona: list[tuple] = field(default_factory=list)
    colonia: list[tuple] = field(default_factory=list)
    paqueteria: list[tuple] = field(default_factory=list)
    usuario: list[tuple] = field(default_factory=list)
    repartidor: list[tuple] = field(default_factory=list)
    manifiesto: list[tuple] = field(default_factory=list)
    paquete: list[tuple] = field(default_factory=list)
    destinatario: list[tuple] = field(default_factory=list)
    ruta: list[tuple] = field(default_factory=list)
    asignacion: list[tuple] = field(default_factory=list)
    entrega: list[tuple] = field(default_factory=list)
    paquete_historial: list[tuple] = field(default_factory=list)
    manifiestos_archivo: dict[date, list[dict]] = field(default_factory=dict)


COLUMNAS = {
    "zona": "zona_id, nombre",
    "colonia": "colonia_id, codigo_postal, nombre, tipo_asentamiento, zona_id",
    "paqueteria": "paqueteria_id, nombre",
    "usuario": "usuario_id, nombre_usuario, nombre_completo, hash_contrasena, rol",
    "repartidor": "usuario_id, zona_id, capacidad_diaria",
    "manifiesto": "manifiesto_id, paqueteria_id, fecha_recepcion, archivo_nombre, importado_por",
    "paquete": "paquete_id, zona_id, colonia_id, manifiesto_id, guia, peso_kg, estado, recibido_en",
    "destinatario": "zona_id, paquete_id, nombre, telefono, calle_numero, referencias",
    "ruta": "ruta_id, zona_id, repartidor_id, fecha, estado",
    "asignacion": "asignacion_id, zona_id, paquete_id, ruta_id, orden, asignado_por, asignado_en",
    "entrega": (
        "entrega_id, asignacion_id, resultado, motivo_fallo, registrada_en, latitud, longitud"
    ),
    "paquete_historial": (
        "zona_id, paquete_id, estado_anterior, estado_nuevo, cambiado_por, cambiado_en"
    ),
}


def leer_catalogo(carpeta: Path = CATALOGOS) -> tuple[list[dict], list[dict]]:
    """Lee zonas.csv y colonias_ags.csv del #9."""
    with open(carpeta / "zonas.csv", encoding="utf-8") as archivo:
        zonas = list(csv.DictReader(archivo))
    with open(carpeta / "colonias_ags.csv", encoding="utf-8") as archivo:
        colonias = list(csv.DictReader(archivo))
    sin_zona = [c["colonia"] for c in colonias if not c["zona_id"]]
    if sin_zona:
        raise SystemExit(f"Hay {len(sin_zona)} colonias sin zona; corre asignar_zonas.py (#9)")
    return zonas, colonias


def a_la_hora(dia: date, hora: int, minuto: int) -> datetime:
    return datetime.combine(dia, time(hora, minuto), tzinfo=ZONA_HORARIA)


def generar(
    zonas: list[dict],
    colonias: list[dict],
    total: int = 100_000,
    semilla: int = 2026,
    hash_contrasena: str = "",
) -> Datos:
    # random basta aquí: son datos de prueba, no llaves ni contraseñas.
    azar = random.Random(semilla)  # nosec B311
    falso = Faker("es_MX")
    falso.seed_instance(semilla)
    datos = Datos()

    # Catálogos: zonas y colonias reales del #9; una sola paquetería.
    for z in zonas:
        datos.zona.append((int(z["zona_id"]), z["nombre"]))
    por_id = {}
    for c in colonias:
        fila = (
            int(c["id_sepomex"]),
            c["codigo_postal"],
            c["colonia"],
            c["tipo_asentamiento"],
            int(c["zona_id"]),
        )
        datos.colonia.append(fila)
        por_id[fila[0]] = fila
    datos.paqueteria.append((1, "J&T Express"))

    # Usuarios: 1 administrador, 3 supervisores y una cuadrilla por zona.
    # La cuadrilla crece con la zona: más colonias, más paquetes, más repartidores.
    hash_ = hash_contrasena or "sin-acceso"
    datos.usuario.append((1, "admin", falso.name(), hash_, "admin"))
    for i in range(1, 4):
        datos.usuario.append((1 + i, f"supervisor{i}", falso.name(), hash_, "supervisor"))
    colonias_por_zona = Counter(fila[4] for fila in datos.colonia)
    repartidores_de: dict[int, list[int]] = defaultdict(list)
    siguiente_id = 5
    for zona_id, _ in datos.zona:
        parte = colonias_por_zona[zona_id] / len(datos.colonia)
        cuantos = max(2, math.ceil(parte * PAQUETES_POR_DIA[1] / (CAPACIDAD * CARGA_OBJETIVO)))
        for _ in range(cuantos):
            usuario = f"rep{siguiente_id - 4:02d}"
            datos.usuario.append((siguiente_id, usuario, falso.name(), hash_, "repartidor"))
            datos.repartidor.append((siguiente_id, zona_id, CAPACIDAD))
            repartidores_de[zona_id].append(siguiente_id)
            siguiente_id += 1

    # Días de recepción: un manifiesto por día hasta llegar al total.
    lista_colonias = list(por_id)
    paquete_id = 0
    dia = PRIMER_DIA
    while paquete_id < total:
        manifiesto_id = len(datos.manifiesto) + 1
        archivo = f"jt_{dia.isoformat()}.csv"
        datos.manifiesto.append((manifiesto_id, 1, dia, archivo, 1))
        cuantos = min(azar.randint(*PAQUETES_POR_DIA), total - paquete_id)
        es_ultimo_dia = paquete_id + cuantos >= total
        del_dia: dict[int, list[tuple]] = defaultdict(list)
        renglones = []
        for consecutivo in range(1, cuantos + 1):
            paquete_id += 1
            colonia = por_id[azar.choice(lista_colonias)]
            zona_id = colonia[4]
            guia = f"JT{dia:%y%m%d}{consecutivo:04d}"
            peso = round(azar.uniform(0.1, 5.0), 2)
            recibido = a_la_hora(dia, 7, azar.randint(0, 59))
            nombre = falso.name()
            telefono = falso.numerify("449#######")
            calle = f"{falso.street_name()} {falso.building_number()}"
            referencia = azar.choice(REFERENCIAS)
            paquete = [
                paquete_id,
                zona_id,
                colonia[0],
                manifiesto_id,
                guia,
                peso,
                "recibido",
                recibido,
            ]
            datos.paquete.append(paquete)
            datos.destinatario.append(
                (zona_id, paquete_id, nombre, telefono, calle, referencia or None)
            )
            datos.paquete_historial.append((zona_id, paquete_id, None, "recibido", 1, recibido))
            del_dia[zona_id].append(paquete)
            renglones.append(
                {
                    "guia": guia,
                    "fecha_recepcion": dia.isoformat(),
                    "destinatario": nombre,
                    "telefono": telefono,
                    "calle_numero": calle,
                    "referencias": referencia,
                    "colonia": colonia[2],
                    "codigo_postal": colonia[1],
                    "peso_kg": peso,
                }
            )
        datos.manifiestos_archivo[dia] = renglones
        # Los paquetes del último día se quedan en "recibido" para poder asignarlos en la app.
        if not es_ultimo_dia:
            repartir_dia(datos, azar, dia, del_dia, repartidores_de, por_id)
        dia += timedelta(days=1)
    return datos


def repartir_dia(
    datos: Datos,
    azar: random.Random,
    dia: date,
    del_dia: dict[int, list[list]],
    repartidores_de: dict[int, list[int]],
    por_id: dict[int, tuple],
) -> None:
    """Asigna los paquetes de cada zona a su cuadrilla, por colonia, y registra la entrega."""
    for zona_id, paquetes in del_dia.items():
        repartidores = repartidores_de[zona_id]
        paquetes.sort(key=lambda p: (por_id[p[2]][1], por_id[p[2]][2], p[0]))
        cargas: dict[int, list[list]] = defaultdict(list)
        for i, paquete in enumerate(paquetes):
            repartidor = repartidores[i % len(repartidores)]
            if len(cargas[repartidor]) < CAPACIDAD:
                cargas[repartidor].append(paquete)
        for repartidor, suyos in cargas.items():
            ruta_id = len(datos.ruta) + 1
            datos.ruta.append((ruta_id, zona_id, repartidor, dia, "cerrada"))
            supervisor = 2 + (zona_id % 3)
            for orden, paquete in enumerate(suyos, start=1):
                asignado = a_la_hora(dia, 8, azar.randint(30, 59))
                salida = a_la_hora(dia, 9, azar.randint(30, 59))
                registrada = a_la_hora(dia, azar.randint(10, 18), azar.randint(0, 59))
                asignacion_id = len(datos.asignacion) + 1
                datos.asignacion.append(
                    (asignacion_id, zona_id, paquete[0], ruta_id, orden, supervisor, asignado)
                )
                if azar.random() < PROBABILIDAD_FALLO:
                    resultado, motivo, latitud, longitud = (
                        "fallido",
                        azar.choice(MOTIVOS_FALLO),
                        None,
                        None,
                    )
                else:
                    resultado, motivo = "entregado", None
                    latitud = round(CENTRO_CIUDAD[0] + azar.uniform(-0.05, 0.05), 6)
                    longitud = round(CENTRO_CIUDAD[1] + azar.uniform(-0.05, 0.05), 6)
                datos.entrega.append(
                    (
                        len(datos.entrega) + 1,
                        asignacion_id,
                        resultado,
                        motivo,
                        registrada,
                        latitud,
                        longitud,
                    )
                )
                paquete[6] = resultado
                pid = paquete[0]
                datos.paquete_historial.extend(
                    [
                        (zona_id, pid, "recibido", "asignado", supervisor, asignado),
                        (zona_id, pid, "asignado", "en_ruta", repartidor, salida),
                        (zona_id, pid, "en_ruta", resultado, repartidor, registrada),
                    ]
                )


def conteo_por_zona(datos: Datos) -> list[dict]:
    """Paquetes por zona: el dato que necesita el ADR-001 (#12)."""
    paquetes = Counter(p[1] for p in datos.paquete)
    colonias = Counter(c[4] for c in datos.colonia)
    dias = len(datos.manifiesto)
    total = len(datos.paquete)
    return [
        {
            "zona_id": zona_id,
            "zona": nombre,
            "colonias": colonias[zona_id],
            "paquetes": paquetes[zona_id],
            "porcentaje": round(100 * paquetes[zona_id] / total, 1),
            "promedio_diario": round(paquetes[zona_id] / dias, 1),
        }
        for zona_id, nombre in datos.zona
    ]


def escribir_salida(datos: Datos, carpeta: Path = SALIDA) -> None:
    """Escribe un manifiesto por día en CSV y en JSON y el conteo por zona."""
    manifiestos = carpeta / "manifiestos"
    manifiestos.mkdir(parents=True, exist_ok=True)
    for dia, renglones in datos.manifiestos_archivo.items():
        nombre = f"jt_{dia.isoformat()}"
        with open(manifiestos / f"{nombre}.csv", "w", newline="", encoding="utf-8") as archivo:
            escritor = csv.DictWriter(archivo, fieldnames=list(renglones[0]))
            escritor.writeheader()
            escritor.writerows(renglones)
        with open(manifiestos / f"{nombre}.json", "w", encoding="utf-8") as archivo:
            json.dump(renglones, archivo, ensure_ascii=False, indent=1)
    conteo = conteo_por_zona(datos)
    with open(carpeta / "conteo_por_zona.csv", "w", newline="", encoding="utf-8") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=list(conteo[0]))
        escritor.writeheader()
        escritor.writerows(conteo)


def cargar(datos: Datos, conninfo: str, reiniciar: bool = False) -> None:  # pragma: no cover
    """Carga todo con COPY en una sola transacción. Si algo falla, no queda nada a medias."""
    import psycopg
    from psycopg import sql

    tablas = list(COLUMNAS)
    with psycopg.connect(conninfo) as conexion, conexion.cursor() as cursor:
        if reiniciar:
            nombres = sql.SQL(", ").join(sql.Identifier(t) for t in tablas)
            cursor.execute(sql.SQL("TRUNCATE {} RESTART IDENTITY CASCADE").format(nombres))
        cursor.execute("SELECT count(*) FROM paquete")
        if cursor.fetchone()[0]:
            raise SystemExit("La base ya tiene paquetes. Usa --reiniciar para vaciarla antes.")
        # El historial ya viene generado; el trigger lo duplicaría al insertar los paquetes.
        cursor.execute("ALTER TABLE paquete DISABLE TRIGGER paquete_historial")
        for tabla in tablas:
            copiar = sql.SQL("COPY {} ({}) FROM STDIN").format(
                sql.Identifier(tabla), sql.SQL(COLUMNAS[tabla])
            )
            with cursor.copy(copiar) as copia:
                for fila in getattr(datos, tabla):
                    copia.write_row(fila)
            print(f"  {tabla}: {len(getattr(datos, tabla))} filas")
        cursor.execute("ALTER TABLE paquete ENABLE TRIGGER paquete_historial")
        # Los id se pusieron a mano: los contadores siguen desde el último.
        for tabla, columna in [
            ("paqueteria", "paqueteria_id"),
            ("usuario", "usuario_id"),
            ("manifiesto", "manifiesto_id"),
            ("paquete", "paquete_id"),
            ("ruta", "ruta_id"),
            ("asignacion", "asignacion_id"),
            ("entrega", "entrega_id"),
        ]:
            consulta = sql.SQL("SELECT setval(pg_get_serial_sequence({}, {}), max({})) FROM {}")
            cursor.execute(
                consulta.format(
                    sql.Literal(tabla),
                    sql.Literal(columna),
                    sql.Identifier(columna),
                    sql.Identifier(tabla),
                )
            )


def conninfo_admin() -> str:  # pragma: no cover
    """Conexión con el usuario administrador del .env (la carga masiva necesita sus permisos)."""
    import psycopg

    return psycopg.conninfo.make_conninfo(
        host=os.environ.get("POSTGRES_HOST_CARGA", "localhost"),
        dbname=os.environ.get("POSTGRES_DB", "zonalia"),
        user=os.environ.get("POSTGRES_ADMIN_USER", ""),
        password=os.environ.get("POSTGRES_ADMIN_PASSWORD", ""),
    )


def main(argumentos: list[str] | None = None) -> None:  # pragma: no cover
    parser = argparse.ArgumentParser(description="Genera los datos sintéticos de Zonalia")
    parser.add_argument("--paquetes", type=int, default=100_000)
    parser.add_argument("--semilla", type=int, default=2026)
    parser.add_argument("--cargar", action="store_true", help="carga los datos a PostgreSQL")
    parser.add_argument("--reiniciar", action="store_true", help="vacía las tablas antes de cargar")
    args = parser.parse_args(argumentos)

    from dotenv import load_dotenv

    from zonalia.api.seguridad import hashear_contrasena

    load_dotenv(RAIZ / ".env")
    # Contraseña de los usuarios de demostración; sin ella nadie puede entrar con ellos.
    contrasena = os.environ.get("CONTRASENA_DEMO") or secrets.token_urlsafe(24)
    zonas, colonias = leer_catalogo()
    datos = generar(zonas, colonias, args.paquetes, args.semilla, hashear_contrasena(contrasena))
    escribir_salida(datos)
    print(f"Paquetes: {len(datos.paquete)} en {len(datos.manifiesto)} días")
    print(
        f"Repartidores: {len(datos.repartidor)} · Rutas: {len(datos.ruta)} · "
        f"Entregas: {len(datos.entrega)}"
    )
    for fila in conteo_por_zona(datos):
        print(
            f"  Zona {fila['zona_id']} {fila['zona']}: {fila['paquetes']} paquetes "
            f"({fila['porcentaje']} %)"
        )
    print(f"Archivos en {SALIDA}")
    if args.cargar:
        print("Cargando a PostgreSQL…")
        cargar(datos, conninfo_admin(), args.reiniciar)
        print("Carga terminada.")
