from pathlib import Path

import pandas as pd

CARPETA = Path(__file__).resolve().parent

def main() -> None:
       colonias = pd.read_csv(CARPETA / "colonias_ags.csv", dtype=str)
       reglas = pd.read_csv(CARPETA / "zonas_por_cp.csv", dtype=str)

       # Cada código postal debe aparecer una sola vez en las reglas.
       repetidos = reglas[reglas["codigo_postal"].duplicated()]["codigo_postal"].tolist()
       if repetidos:
           raise SystemExit(f"Códigos postales repetidos en zonas_por_cp.csv: {repetidos}")

       zona_por_cp = dict(zip(reglas["codigo_postal"], reglas["zona_id"], strict=True))
       colonias["zona_id"] = colonias["codigo_postal"].map(zona_por_cp).fillna("")

       colonias.to_csv(CARPETA / "colonias_ags.csv", index=False, encoding="utf-8")
       sin_zona = (colonias["zona_id"] == "").sum()
       print(f"Colonias con zona: {len(colonias) - sin_zona} de {len(colonias)}")
       print(f"Colonias sin zona: {sin_zona}")

if __name__ == "__main__":
       main()