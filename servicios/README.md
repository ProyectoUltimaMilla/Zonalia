# servicios

Servicios en Python 3.12 (lineamientos IV-b y IV-e1): API REST (FastAPI), dominio en POO, acceso a datos, limpieza con pandas, análisis y gráficas, y generador de datos sintéticos. Responsable principal: Jesús (API) y Tadeo (datos y análisis).

- Se crea en el issue #7 (esqueleto) y la CI en el #8.
- Las pruebas van en `servicios/tests/` (cobertura mínima de 60 %, IV-f2).
- Los datos que genera el generador van en `servicios/salida/`, que no se sube (se regeneran con semilla fija).

## Cómo crear el entorno

Desde la carpeta `servicios`, con Python 3.12:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -e ".[dev]"
```

En macOS o Linux: `python3.12 -m venv .venv` y `source .venv/bin/activate`.

## Cómo probar

```powershell
ruff check .
ruff format --check .
pytest
uvicorn zonalia.api.main:app --reload
```

La API queda en http://127.0.0.1:8000/health y la documentación en http://127.0.0.1:8000/docs.
