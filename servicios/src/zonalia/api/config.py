"""Configuración de la API. Todo sale de variables de entorno (.env), nunca del código."""

import os
from dataclasses import dataclass
from functools import lru_cache


@dataclass(frozen=True)
class Config:
    jwt_secreto: str
    jwt_minutos_expiracion: int
    cors_origenes: list[str]


@lru_cache
def obtener_config() -> Config:
    """Lee la configuración una sola vez. Falla al arrancar si falta el secreto del JWT."""
    secreto = os.environ.get("JWT_SECRETO", "")
    if len(secreto) < 32:
        raise RuntimeError("JWT_SECRETO debe existir en el .env y tener al menos 32 caracteres")
    origenes = os.environ.get("CORS_ORIGENES", "")
    return Config(
        jwt_secreto=secreto,
        jwt_minutos_expiracion=int(os.environ.get("JWT_MINUTOS_EXPIRACION", "480")),
        cors_origenes=[o.strip() for o in origenes.split(",") if o.strip()],
    )
