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

Generador de datos sintéticos (#15)

Crea 100 000 paquetes ficticios con semilla fija (la misma semilla da siempre los mismos datos): destinatarios inventados con Faker, un manifiesto por día en CSV y JSON, rutas, asignaciones, entregas y el historial de estados. Las colonias y zonas son las del catálogo de db/catalogos/ (#9). Ningún dato es real.

python -m zonalia.generador                       # solo genera los archivos en servicios/salida/
python -m zonalia.generador --cargar              # además los carga a la base (debe estar vacía)
python -m zonalia.generador --cargar --reiniciar  # vacía las tablas y vuelve a cargar

Para cargar, la base del compose debe estar arriba (docker compose --profile local up -d db). Se conecta con POSTGRES_ADMIN_USER y POSTGRES_ADMIN_PASSWORD del .env.

CONTRASENA_DEMO del .env es la contraseña de los usuarios de demostración (admin, supervisor1 a supervisor3, rep01 en adelante). Si está vacía, nadie puede entrar con ellos.

En servicios/salida/ quedan manifiestos/jt_AAAA-MM-DD.csv y .json, y conteo_por_zona.csv, que usa el ADR-001 (#12). La carpeta no se sube.