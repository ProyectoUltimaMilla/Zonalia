"""Variables de entorno de prueba. Se cargan antes de importar la API."""

import os

os.environ.setdefault("JWT_SECRETO", "secreto-solo-para-pruebas-de-32-caracteres-o-mas")
os.environ.setdefault("JWT_MINUTOS_EXPIRACION", "60")
os.environ.setdefault("CORS_ORIGENES", "https://zonalia.local")
