"""Pruebas del generador de datos sintéticos (#15). No necesitan base de datos."""

import csv
from collections import Counter
from pathlib import Path

import pytest

from zonalia.generador.generar import CAPACIDAD, conteo_por_zona, escribir_salida, generar

ZONAS = [{"zona_id": "1", "nombre": "Centro"}, {"zona_id": "2", "nombre": "Norte"}]
COLONIAS = [
    {
        "id_sepomex": "1",
        "codigo_postal": "20000",
        "colonia": "Centro",
        "tipo_asentamiento": "Colonia",
        "zona_id": "1",
    },
    {
        "id_sepomex": "2",
        "codigo_postal": "20010",
        "colonia": "Las Brisas",
        "tipo_asentamiento": "Fraccionamiento",
        "zona_id": "1",
    },
    {
        "id_sepomex": "3",
        "codigo_postal": "20100",
        "colonia": "Pocitos",
        "tipo_asentamiento": "Colonia",
        "zona_id": "2",
    },
    {
        "id_sepomex": "4",
        "codigo_postal": "20110",
        "colonia": "Norte Uno",
        "tipo_asentamiento": "Fraccionamiento",
        "zona_id": "2",
    },
]


@pytest.fixture(scope="module")
def datos():
    return generar(ZONAS, COLONIAS, total=3000, semilla=7)


def test_genera_el_total_pedido(datos) -> None:
    assert len(datos.paquete) == 3000
    assert len(datos.destinatario) == 3000
    assert len({p[4] for p in datos.paquete}) == 3000  # guías únicas


def test_misma_semilla_mismos_datos(datos) -> None:
    otra = generar(ZONAS, COLONIAS, total=3000, semilla=7)
    assert otra.paquete == datos.paquete
    assert otra.destinatario == datos.destinatario


def test_la_zona_del_paquete_es_la_de_su_colonia(datos) -> None:
    zona_de = {int(c["id_sepomex"]): int(c["zona_id"]) for c in COLONIAS}
    assert all(p[1] == zona_de[p[2]] for p in datos.paquete)


def test_ningun_repartidor_pasa_su_capacidad(datos) -> None:
    por_ruta = Counter(a[3] for a in datos.asignacion)
    assert max(por_ruta.values()) <= CAPACIDAD


def test_estados_consistentes(datos) -> None:
    asignados = {a[2] for a in datos.asignacion}
    for paquete in datos.paquete:
        if paquete[0] in asignados:
            assert paquete[6] in ("entregado", "fallido")
        else:
            assert paquete[6] == "recibido"
    assert all(e[3] for e in datos.entrega if e[2] == "fallido")  # todo fallo tiene motivo
    ultimo = {}
    for h in datos.paquete_historial:
        ultimo[h[1]] = h[3]
    assert all(ultimo[p[0]] == p[6] for p in datos.paquete)


def test_destinatarios_ficticios_con_telefono_de_aguascalientes(datos) -> None:
    for d in datos.destinatario:
        assert d[3].startswith("449")
        assert len(d[3]) == 10


def test_escribe_manifiestos_y_conteo(datos, tmp_path: Path) -> None:
    escribir_salida(datos, tmp_path)
    archivos = list((tmp_path / "manifiestos").glob("*.csv"))
    assert len(archivos) == len(datos.manifiesto)
    assert len(list((tmp_path / "manifiestos").glob("*.json"))) == len(datos.manifiesto)
    with open(tmp_path / "conteo_por_zona.csv", encoding="utf-8") as archivo:
        filas = list(csv.DictReader(archivo))
    assert sum(int(f["paquetes"]) for f in filas) == 3000
    assert [f["zona"] for f in filas] == ["Centro", "Norte"]
    assert conteo_por_zona(datos)[0]["paquetes"] == int(filas[0]["paquetes"])
