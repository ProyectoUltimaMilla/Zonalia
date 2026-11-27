import sys
from pathlib import Path

import pandas as pd

CARPETA = Path(__file__).resolve().parent

def main() -> int:
       colonias = pd.read_csv(CARPETA / "colonias_ags.csv", dtype=str, keep_default_na=False)
       zonas = pd.read_csv(CARPETA / "zonas.csv", dtype=str, keep_default_na=False)

       sin_zona = colonias[colonias["zona_id"] == ""]
       zona_inexistente = colonias[
           (colonias["zona_id"] != "") & ~colonias["zona_id"].isin(zonas["zona_id"])
       ]
       por_zona = colonias["zona_id"].value_counts()
       zonas_vacias = [z for z in zonas["zona_id"] if z not in por_zona.index]

       print(f"Colonias en el catálogo: {len(colonias)}")
       print(f"Colonias sin zona: {len(sin_zona)}")
       print(f"Colonias con una zona que no existe en zonas.csv: {len(zona_inexistente)}")
       print("\nColonias por zona:")
       for fila in zonas.itertuples():
           print(f"  {fila.zona_id} {fila.nombre}: {por_zona.get(fila.zona_id, 0)}")

       problemas = len(sin_zona) + len(zona_inexistente) + len(zonas_vacias)
       if problemas:
           print("\nHay problemas. Ejemplos de colonias sin zona:")
           print(sin_zona.head(10).to_string(index=False))
           if zonas_vacias:
               print(f"Zonas sin ninguna colonia: {zonas_vacias}")
           return 1
       print("\nTodo bien: cada colonia tiene una zona válida y ninguna zona está vacía.")
       return 0

if __name__ == "__main__":
       sys.exit(main())