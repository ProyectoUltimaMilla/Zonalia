"""Pruebas de repositorios y endpoints de paquetes (#21). No necesitan base de datos:
la conexión es un objeto falso que recuerda si se hizo commit, rollback y close."""

from datetime import date, datetime

import psycopg
import pytest
from fastapi.testclient import TestClient

from zonalia.api.main import app
from zonalia.api.paquetes import obtener_repositorio_asignaciones, obtener_repositorio_paquetes
from zonalia.api.seguridad import crear_token
from zonalia.datos.paquetes import (
    AsignacionHecha,
    PaqueteResumen,
    RepositorioAsignaciones,
    RepositorioPaquetes,
    ZonaResumen,
    traducir_error,
)
from zonalia.dominio.errores import (
    RepartidorSaturadoError,
    TransicionInvalidaError,
    ZonaNoEncontradaError,
)


class ErrorDeLaBase(psycopg.Error):
    """Simula el error que lanza asignar_paquete con su código ZN00x."""

    def __init__(self, codigo: str) -> None:
        self._codigo = codigo
        super().__init__(f"error {codigo}")

    @property
    def sqlstate(self) -> str:  # type: ignore[override]
        return self._codigo


class CursorFalso:
    def __init__(self, conexion: "ConexionFalsa") -> None:
        self._conexion = conexion

    def __enter__(self) -> "CursorFalso":
        return self

    def __exit__(self, *args: object) -> None:
        return None

    def execute(self, consulta: str, parametros: tuple) -> None:
        self._conexion.consultas.append((consulta, parametros))
        if consulta.startswith("CALL") and self._conexion.error:
            raise self._conexion.error

    def fetchone(self) -> tuple:
        return (7,)


class ConexionFalsa:
    def __init__(self, error: psycopg.Error | None = None) -> None:
        self.error = error
        self.consultas: list[tuple] = []
        self.hizo_commit = self.hizo_rollback = self.cerrada = False

    def cursor(self) -> CursorFalso:
        return CursorFalso(self)

    def commit(self) -> None:
        self.hizo_commit = True

    def rollback(self) -> None:
        self.hizo_rollback = True

    def close(self) -> None:
        self.cerrada = True


HOY = date(2026, 11, 26)


def test_asignacion_correcta_hace_commit_y_cierra():
    conexion = ConexionFalsa()
    hecha = RepositorioAsignaciones(lambda: conexion).asignar(3, 100, 9, 1, HOY)
    assert hecha == AsignacionHecha(3, 100, 9, HOY, 7)
    assert conexion.hizo_commit and not conexion.hizo_rollback and conexion.cerrada
    consulta, parametros = conexion.consultas[0]
    assert consulta == "CALL asignar_paquete(%s, %s, %s, %s, %s)"  # parametrizada
    assert parametros == (3, 100, 9, 1, HOY)


def test_repartidor_saturado_hace_rollback():
    conexion = ConexionFalsa(ErrorDeLaBase("ZN002"))
    with pytest.raises(RepartidorSaturadoError):
        RepositorioAsignaciones(lambda: conexion).asignar(3, 100, 9, 1, HOY)
    assert conexion.hizo_rollback and not conexion.hizo_commit and conexion.cerrada


def test_traducir_error():
    assert isinstance(traducir_error(ErrorDeLaBase("ZN001")), TransicionInvalidaError)
    assert isinstance(traducir_error(ErrorDeLaBase("ZN004")), ZonaNoEncontradaError)
    desconocido = ErrorDeLaBase("23505")
    assert traducir_error(desconocido) is desconocido


class ConexionLectura:
    def __init__(self, filas: list[tuple]) -> None:
        self.filas = filas
        self.parametros: object = None

    def __enter__(self) -> "ConexionLectura":
        return self

    def __exit__(self, *args: object) -> None:
        return None

    def execute(self, consulta: str, parametros: object) -> "ConexionLectura":
        self.parametros = parametros
        return self

    def fetchall(self) -> list[tuple]:
        return self.filas


def test_repositorio_paquetes_lee_zonas_y_paquetes():
    zonas = RepositorioPaquetes(lambda: ConexionLectura([(1, "Centro", 12)])).zonas()
    assert zonas == [ZonaResumen(1, "Centro", 12)]
    conexion = ConexionLectura([(5, 2, "JT000005", "recibido", "Bosques", "20120", datetime.now())])
    paquetes = RepositorioPaquetes(lambda: conexion).paquetes(2, "recibido", 10)
    assert paquetes[0].guia == "JT000005"
    assert conexion.parametros == {"zona": 2, "estado": "recibido", "limite": 10}


class RepositorioPaquetesFalso:
    def zonas(self) -> list[ZonaResumen]:
        return [ZonaResumen(1, "Centro", 3)]

    def paquetes(self, zona_id: int | None, estado: str | None, limite: int):
        return [PaqueteResumen(1, 1, "JT000001", "recibido", "Centro", "20000", datetime.now())]


class RepositorioAsignacionesFalso:
    def __init__(self, error: Exception | None = None) -> None:
        self.error = error

    def asignar(self, zona_id, paquete_id, repartidor_id, asignado_por, fecha):
        if self.error:
            raise self.error
        return AsignacionHecha(zona_id, paquete_id, repartidor_id, fecha, 1)


@pytest.fixture
def cliente():
    app.dependency_overrides[obtener_repositorio_paquetes] = RepositorioPaquetesFalso
    asignaciones = RepositorioAsignacionesFalso()
    app.dependency_overrides[obtener_repositorio_asignaciones] = lambda: asignaciones
    yield TestClient(app)
    app.dependency_overrides.clear()


def encabezado(rol: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {crear_token(1, 'demo', rol)}"}


def test_zonas_pide_token(cliente):
    assert cliente.get("/zonas").status_code == 401
    respuesta = cliente.get("/zonas", headers=encabezado("repartidor"))
    assert respuesta.status_code == 200
    assert respuesta.json()[0]["nombre"] == "Centro"


def test_paquetes_solo_admin_y_supervisor(cliente):
    assert cliente.get("/paquetes", headers=encabezado("repartidor")).status_code == 403
    respuesta = cliente.get("/paquetes?zona_id=1&estado=recibido", headers=encabezado("supervisor"))
    assert respuesta.status_code == 200
    assert respuesta.json()[0]["guia"] == "JT000001"
    assert cliente.get("/paquetes?estado=perdido", headers=encabezado("admin")).status_code == 422


def test_crear_asignacion(cliente):
    cuerpo = {"zona_id": 1, "paquete_id": 1, "repartidor_id": 5, "fecha": "2026-11-26"}
    respuesta = cliente.post("/asignaciones", json=cuerpo, headers=encabezado("supervisor"))
    assert respuesta.status_code == 201
    assert respuesta.json()["carga_del_dia"] == 1


@pytest.mark.parametrize(
    ("error", "codigo"),
    [
        (RepartidorSaturadoError("lleno"), 409),
        (ZonaNoEncontradaError("no existe"), 404),
        (TransicionInvalidaError("ya asignado"), 409),
    ],
)
def test_errores_de_asignacion(cliente, error, codigo):
    app.dependency_overrides[obtener_repositorio_asignaciones] = lambda: (
        RepositorioAsignacionesFalso(error)
    )
    cuerpo = {"zona_id": 1, "paquete_id": 1, "repartidor_id": 5}
    respuesta = cliente.post("/asignaciones", json=cuerpo, headers=encabezado("admin"))
    assert respuesta.status_code == codigo
