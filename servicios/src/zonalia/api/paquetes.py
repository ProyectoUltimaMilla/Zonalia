"""Endpoints de zonas, paquetes y asignaciones (#21)."""

from datetime import date
from typing import Annotated, Literal

import psycopg
from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel

from zonalia.api.seguridad import UsuarioActual, requiere_rol, usuario_actual
from zonalia.datos.paquetes import (
    AsignacionHecha,
    PaqueteResumen,
    RepositorioAsignaciones,
    RepositorioPaquetes,
    ZonaResumen,
)
from zonalia.datos.usuarios import conninfo_desde_entorno
from zonalia.dominio.errores import (
    RepartidorSaturadoError,
    TransicionInvalidaError,
    ZonaNoEncontradaError,
)

router = APIRouter(tags=["paquetes"])

Estado = Literal["recibido", "asignado", "en_ruta", "entregado", "fallido", "devuelto"]


def _conectar() -> psycopg.Connection:
    return psycopg.connect(conninfo_desde_entorno())


def obtener_repositorio_paquetes() -> RepositorioPaquetes:
    return RepositorioPaquetes(_conectar)


def obtener_repositorio_asignaciones() -> RepositorioAsignaciones:
    return RepositorioAsignaciones(_conectar)


class NuevaAsignacion(BaseModel):
    zona_id: int
    paquete_id: int
    repartidor_id: int
    fecha: date | None = None


@router.get("/zonas")
def listar_zonas(
    _: Annotated[UsuarioActual, Depends(usuario_actual)],
    repositorio: Annotated[RepositorioPaquetes, Depends(obtener_repositorio_paquetes)],
) -> list[ZonaResumen]:
    """Zonas activas con cuántos paquetes tiene cada una por asignar."""
    return repositorio.zonas()


@router.get("/paquetes")
def listar_paquetes(
    _: Annotated[UsuarioActual, Depends(requiere_rol("admin", "supervisor"))],
    repositorio: Annotated[RepositorioPaquetes, Depends(obtener_repositorio_paquetes)],
    zona_id: Annotated[int | None, Query(ge=1)] = None,
    estado: Estado | None = None,
    limite: Annotated[int, Query(ge=1, le=500)] = 50,
) -> list[PaqueteResumen]:
    """Paquetes más recientes, filtrados por zona y estado."""
    return repositorio.paquetes(zona_id, estado, limite)


@router.post("/asignaciones", status_code=status.HTTP_201_CREATED)
def crear_asignacion(
    datos: NuevaAsignacion,
    usuario: Annotated[UsuarioActual, Depends(requiere_rol("admin", "supervisor"))],
    repositorio: Annotated[RepositorioAsignaciones, Depends(obtener_repositorio_asignaciones)],
) -> AsignacionHecha:
    """Asigna un paquete a la ruta del día de un repartidor de su misma zona."""
    try:
        return repositorio.asignar(
            datos.zona_id,
            datos.paquete_id,
            datos.repartidor_id,
            usuario.usuario_id,
            datos.fecha or date.today(),
        )
    except RepartidorSaturadoError as error:
        raise HTTPException(status.HTTP_409_CONFLICT, str(error)) from error
    except ZonaNoEncontradaError as error:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(error)) from error
    except TransicionInvalidaError as error:
        raise HTTPException(status.HTTP_409_CONFLICT, str(error)) from error
