"""Acceso a los usuarios de la base. La API depende de la interfaz, no de PostgreSQL."""

import os
from dataclasses import dataclass
from typing import Protocol

import psycopg


@dataclass(frozen=True)
class UsuarioGuardado:
    usuario_id: int
    nombre_usuario: str
    hash_contrasena: str
    rol: str
    activo: bool


class RepositorioUsuarios(Protocol):
    def buscar_por_nombre(self, nombre_usuario: str) -> UsuarioGuardado | None: ...


class RepositorioUsuariosPostgres:
    """Lee la tabla usuario con una consulta parametrizada (nunca se arma SQL con texto)."""

    def __init__(self, conninfo: str) -> None:
        self._conninfo = conninfo

    def buscar_por_nombre(self, nombre_usuario: str) -> UsuarioGuardado | None:
        with psycopg.connect(self._conninfo) as conexion:
            fila = conexion.execute(
                "SELECT usuario_id, nombre_usuario, hash_contrasena, rol, activo "
                "FROM usuario WHERE nombre_usuario = %s",
                (nombre_usuario,),
            ).fetchone()
        return UsuarioGuardado(*fila) if fila else None


def conninfo_desde_entorno() -> str:
    """Arma la conexión con las variables del .env. Usa el primer host de POSTGRES_HOSTS."""
    host = os.environ.get("POSTGRES_HOSTS", "localhost").split(",")[0].strip()
    return psycopg.conninfo.make_conninfo(
        host=host,
        dbname=os.environ.get("POSTGRES_DB", "zonalia"),
        user=os.environ.get("POSTGRES_API_USER", ""),
        password=os.environ.get("POSTGRES_API_PASSWORD", ""),
    )
