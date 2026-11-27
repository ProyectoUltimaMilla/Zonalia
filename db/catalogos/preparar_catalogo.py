from pathlib import Path

import pandas as pd

CARPETA = Path(__file__).resolve().parent
ORIGEN = CARPETA / "CPdescarga_ags.txt"
DESTINO = CARPETA / "colonias_ags.csv"
REGLAS = CARPETA / "zonas_por_cp.csv"

# Columnas del TXT de SEPOMEX que usamos y el nombre que les damos.
COLUMNAS = {
    "id_asenta_cpcons": "id_sepomex",
    "d_codigo": "codigo_postal",
    "d_asenta": "colonia",
    "d_tipo_asenta": "tipo_asentamiento",
}

def main() -> None:
    # 1. Leer: separado por |, en latin-1 y sin la primera línea (es un aviso legal).
    #    dtype=str para que los códigos postales no pierdan ceros a la izquierda.
    datos = pd.read_csv(ORIGEN, sep="|", encoding="latin-1", skiprows=1, dtype=str)

    # 2. Quitar espacios sobrantes al inicio y al final de cada texto.
    datos = datos.apply(lambda columna: columna.str.strip())

    # 3. Quedarnos solo con la ciudad de Aguascalientes (municipio y ciudad).
    ciudad = datos[(datos["D_mnpio"] == "Aguascalientes") & (datos["d_ciudad"] == "Aguascalientes")]

    # 4. Elegir y renombrar columnas, quitar repetidos y ordenar.
    colonias = (
        ciudad[list(COLUMNAS)]
        .rename(columns=COLUMNAS)
        .drop_duplicates()
        .sort_values(["codigo_postal", "colonia"])
    )

    # 5. Columna de zona vacía: se llena con el criterio que decida el equipo.
    colonias["zona_id"] = ""

    colonias.to_csv(DESTINO, index=False, encoding="utf-8")

    # 6. Plantilla para asignar zonas por código postal (una fila por CP).
    #    Solo se crea si no existe, para no borrar lo que el equipo ya llenó.
    if not REGLAS.exists():
        plantilla = (
            colonias.groupby("codigo_postal")
            .agg(colonias=("colonia", "count"), ejemplos=("colonia", lambda c: "; ".join(c[:3])))
            .reset_index()
        )
        plantilla["zona_id"] = ""
        plantilla.to_csv(REGLAS, index=False, encoding="utf-8")
        print(f"Plantilla generada: {REGLAS.name} ({len(plantilla)} códigos postales)")

    print(f"Filas leídas del TXT: {len(datos)}")
    print(f"Colonias de la ciudad de Aguascalientes: {len(colonias)}")
    print(f"Códigos postales distintos: {colonias['codigo_postal'].nunique()}")
    print(f"Archivo generado: {DESTINO.name}")

if __name__ == "__main__":
    main()