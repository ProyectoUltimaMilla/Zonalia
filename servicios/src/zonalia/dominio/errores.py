"""Excepciones del dominio de Zonalia (#20).

La API las traduce a respuestas HTTP y la capa de datos traduce a ellas los errores ZN00x
de PostgreSQL (ver db/esquema/004_funciones.sql).
"""


class ZonaliaError(Exception):
    """Base de todos los errores de negocio. Atraparla atrapa a todos."""


class ZonaNoEncontradaError(ZonaliaError):
    """La colonia o el código postal no pertenecen a ninguna zona del catálogo (ZN004)."""


class RepartidorSaturadoError(ZonaliaError):
    """El repartidor ya llegó a su capacidad del día (ZN002)."""


class DireccionInvalidaError(ZonaliaError):
    """La dirección viene incompleta o con un código postal mal escrito."""


class TransicionInvalidaError(ZonaliaError):
    """El paquete no puede pasar de su estado actual al que se pide (ZN001, ZN003)."""
