"""Pruebas del modelo de dominio (#20). No usan base de datos."""

from datetime import date, datetime

import pytest

from zonalia.dominio.clasificador import Clasificador, normalizar
from zonalia.dominio.errores import (
    DireccionInvalidaError,
    RepartidorSaturadoError,
    TransicionInvalidaError,
    ZonaliaError,
    ZonaNoEncontradaError,
)
from zonalia.dominio.modelos import (
    Administrador,
    Colonia,
    Entrega,
    Paquete,
    Repartidor,
    Ruta,
    Supervisor,
    Zona,
    usuario_desde_rol,
)

COLONIAS = [
    Colonia(1, "20000", "Aguascalientes Centro", "Colonia", 1),
    Colonia(5, "20010", "Colinas del Río", "Fraccionamiento", 5),
    Colonia(6, "20010", "Olivares Santana", "Colonia", 5),
    Colonia(16, "20020", "Buenos Aires", "Colonia", 1),
]


def paquete(numero: int, zona: int = 5, estado: str = "recibido") -> Paquete:
    return Paquete(numero, zona, 5, f"JT{numero:06d}", estado)


def test_todos_los_errores_heredan_de_zonalia_error():
    for clase in (ZonaNoEncontradaError, RepartidorSaturadoError, DireccionInvalidaError):
        assert issubclass(clase, ZonaliaError)


def test_zona_es_inmutable():
    zona = Zona(1, "Centro")
    with pytest.raises(AttributeError):
        zona.nombre = "Otro"  # type: ignore[misc]


def test_colonia_rechaza_codigo_postal_mal_escrito():
    with pytest.raises(DireccionInvalidaError):
        Colonia(99, "2001", "Sin CP", "Colonia", 1)


def test_transiciones_permitidas_y_prohibidas():
    p = paquete(1)
    assert p.asignable
    p.cambiar_estado("asignado")
    p.cambiar_estado("en_ruta")
    p.cambiar_estado("fallido")
    assert p.asignable  # un fallido se puede volver a asignar
    p.cambiar_estado("devuelto")
    assert not p.asignable
    with pytest.raises(TransicionInvalidaError):
        p.cambiar_estado("asignado")


def test_no_se_salta_estados():
    with pytest.raises(TransicionInvalidaError):
        paquete(2).cambiar_estado("entregado")


def test_roles_y_permisos():
    admin = Administrador(1, "admin", "Admin Demo")
    supervisor = Supervisor(2, "supervisor1", "Supervisor Demo")
    repartidor = Repartidor(3, "rep01", "Repartidor Demo", zona_id=5)
    assert (admin.rol, supervisor.rol, repartidor.rol) == ("admin", "supervisor", "repartidor")
    assert admin.puede_asignar() and supervisor.puede_asignar()
    assert not repartidor.puede_asignar()
    assert repr(repartidor) == "Repartidor('rep01')"
    assert repartidor.capacidad_diaria == 60


def test_usuario_desde_rol():
    assert isinstance(usuario_desde_rol("admin", 1, "a", "A"), Administrador)
    assert isinstance(usuario_desde_rol("supervisor", 2, "s", "S"), Supervisor)
    with pytest.raises(ValueError):
        usuario_desde_rol("repartidor", 3, "r", "R")


def test_ruta_agrega_hasta_la_capacidad():
    repartidor = Repartidor(3, "rep01", "Repartidor Demo", zona_id=5, capacidad_diaria=2)
    ruta = Ruta(repartidor, date(2026, 11, 26))
    ruta.agregar(paquete(1))
    ruta.agregar(paquete(2))
    assert ruta.carga == 2
    assert all(p.estado == "asignado" for p in ruta.paquetes)
    tercero = paquete(3)
    with pytest.raises(RepartidorSaturadoError):
        ruta.agregar(tercero)
    assert tercero.estado == "recibido"  # no se tocó


def test_ruta_rechaza_paquete_de_otra_zona():
    ruta = Ruta(Repartidor(3, "rep01", "R", zona_id=5), date(2026, 11, 26))
    with pytest.raises(TransicionInvalidaError):
        ruta.agregar(paquete(1, zona=1))


def test_entrega_fallida_necesita_motivo():
    ahora = datetime(2026, 11, 26, 12, 0)
    assert Entrega(paquete(1), "entregado", ahora).motivo_fallo is None
    assert Entrega(paquete(2), "fallido", ahora, "Nadie en el domicilio").motivo_fallo
    with pytest.raises(TransicionInvalidaError):
        Entrega(paquete(3), "fallido", ahora)
    with pytest.raises(TransicionInvalidaError):
        Entrega(paquete(4), "perdido", ahora)


def test_normalizar_quita_acentos_mayusculas_y_espacios():
    assert normalizar("  Colinas   del RÍO ") == "colinas del rio"


def test_clasificador_encuentra_la_zona():
    clasificador = Clasificador(COLONIAS)
    assert clasificador.zona("20010", "colinas del rio") == 5
    assert clasificador.zona(" 20000 ", "AGUASCALIENTES CENTRO") == 1
    assert clasificador.colonia("20020", "Buenos Aires").colonia_id == 16
    assert clasificador.zona_por_cp("20010") == 5


def test_clasificador_errores():
    clasificador = Clasificador(COLONIAS)
    with pytest.raises(DireccionInvalidaError):
        clasificador.zona("2001", "Colinas del Río")
    with pytest.raises(DireccionInvalidaError):
        clasificador.zona("20010", "   ")
    with pytest.raises(ZonaNoEncontradaError):
        clasificador.zona("20010", "Buenos Aires")  # existe, pero en otro CP
    with pytest.raises(ZonaNoEncontradaError):
        clasificador.zona_por_cp("99999")
