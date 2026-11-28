"""Repositorios de zonas, paquetes y asignaciones con DB-API (psycopg) (#21).

Todo el SQL va parametrizado con %s: los valores nunca se pegan al texto de la consulta.
La asignación usa el procedimiento asignar_paquete del #11 dentro de una transacción.
"""

from collections.abc import Callable
from dataclasses import dataclass
from datetime import date, datetime
from typing import Any, Protocol

import psycopg

from zonalia.dominio.errores import (
    RepartidorSaturadoError,
    TransicionInvalidaError,
    ZonaliaError,
    ZonaNoEncontradaError,
)

# Errores propios de la base (004_funciones.sql) -> excepción del dominio (#20).
ERRORES_DE_LA_BASE: dict[str, type[ZonaliaError]] = {
    "ZN001": TransicionInvalidaError,
    "ZN002": RepartidorSaturadoError,
    "ZN003": TransicionInvalidaError,
    "ZN004": ZonaNoEncontradaError,
    "ZN005": TransicionInvalidaError,
    "ZN006": ZonaNoEncontradaError,
}


@dataclass(frozen=True)
class ZonaResumen:
    zona_id: int
    nombre: str
    paquetes_por_asignar: int


@dataclass(frozen=True)
class PaqueteResumen:
    paquete_id: int
    zona_id: int
    guia: str
    estado: str
    colonia: str
    codigo_postal: str
    recibido_en: datetime


@dataclass(frozen=True)
class AsignacionHecha:
    zona_id: int
    paquete_id: int
    repartidor_id: int
    fecha: date
    carga_del_dia: int


class Conectar(Protocol):
    def __call__(self) -> Any: ...


def traducir_error(error: psycopg.Error) -> Exception:
    """Convierte un error ZN00x de la base en la excepción del dominio que le toca."""
    clase = ERRORES_DE_LA_BASE.get(error.sqlstate or "")
    if clase is None:
        return error
    mensaje = error.diag.message_primary if error.diag else None
    return clase(mensaje or str(error))


class RepositorioPaquetes:
    """Consultas de lectura de zonas y paquetes."""

    def __init__(self, conectar: Callable[[], Any]) -> None:
        self._conectar = conectar

    def zonas(self) -> list[ZonaResumen]:
        with self._conectar() as conexion:
            filas = conexion.execute(
                "SELECT z.zona_id, z.nombre, count(p.paquete_id) "
                "FROM zona z "
                "LEFT JOIN paquete p ON p.zona_id = z.zona_id AND p.estado = %s "
                "WHERE z.activa "
                "GROUP BY z.zona_id, z.nombre ORDER BY z.zona_id",
                ("recibido",),
            ).fetchall()
        return [ZonaResumen(*fila) for fila in filas]

    def paquetes(
        self, zona_id: int | None = None, estado: str | None = None, limite: int = 50
    ) -> list[PaqueteResumen]:
        """Paquetes filtrados por zona y estado. Con zona_id solo lee su fragmento."""
        with self._conectar() as conexion:
            filas = conexion.execute(
                "SELECT p.paquete_id, p.zona_id, p.guia, p.estado, c.nombre, c.codigo_postal, "
                "p.recibido_en "
                "FROM paquete p JOIN colonia c ON c.colonia_id = p.colonia_id "
                "WHERE (%(zona)s::smallint IS NULL OR p.zona_id = %(zona)s) "
                "AND (%(estado)s::text IS NULL OR p.estado = %(estado)s) "
                "ORDER BY p.recibido_en DESC, p.paquete_id DESC "
                "LIMIT %(limite)s",
                {"zona": zona_id, "estado": estado, "limite": limite},
            ).fetchall()
        return [PaqueteResumen(*fila) for fila in filas]


class RepositorioAsignaciones:
    """Asigna paquetes a repartidores en una transacción explícita."""

    def __init__(self, conectar: Callable[[], Any]) -> None:
        self._conectar = conectar

    def asignar(
        self, zona_id: int, paquete_id: int, repartidor_id: int, asignado_por: int, fecha: date
    ) -> AsignacionHecha:
        """Llama a asignar_paquete. Si la base rechaza, rollback y error del dominio."""
        conexion = self._conectar()
        try:
            with conexion.cursor() as cursor:
                cursor.execute(
                    "CALL asignar_paquete(%s, %s, %s, %s, %s)",
                    (zona_id, paquete_id, repartidor_id, asignado_por, fecha),
                )
                cursor.execute("SELECT carga_repartidor(%s, %s)", (repartidor_id, fecha))
                carga = cursor.fetchone()[0]
        except psycopg.Error as error:
            conexion.rollback()  # nada de lo que hizo el CALL queda guardado
            raise traducir_error(error) from error
        else:
            conexion.commit()  # solo si todo salió bien
            return AsignacionHecha(zona_id, paquete_id, repartidor_id, fecha, carga)
        finally:
            conexion.close()  # pase lo que pase, la conexión se cierra
