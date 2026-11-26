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

## Variables de entorno

La API lee su configuración del `.env` de la raíz del repo (copia de `.env.example`, nunca se sube). Para correrla en tu laptop necesitas al menos:

- `JWT_SECRETO`: texto aleatorio de 32 caracteres o más. Genéralo con `python -c "import secrets; print(secrets.token_urlsafe(48))"`.
- `CORS_ORIGENES`: los orígenes web que pueden llamar a la API, separados por comas (en desarrollo, `http://localhost:5173`).

Las pruebas no necesitan `.env`: `tests/conftest.py` pone valores de prueba.

## Cómo probar

```powershell
ruff check .
ruff format --check .
pytest
uvicorn zonalia.api.main:app --reload --env-file ../.env
```

La API queda en http://127.0.0.1:8000/health y la documentación en http://127.0.0.1:8000/docs.

El inicio de sesión (`POST /auth/login`) y `GET /auth/yo` aparecen en `/docs`. Para probarlos con la base, levanta `db` con el compose y da de alta un usuario con el hash que genera `python -m zonalia.api.seguridad` (pide la contraseña sin mostrarla).
