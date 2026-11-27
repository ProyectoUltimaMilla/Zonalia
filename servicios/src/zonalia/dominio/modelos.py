"""Modelo de dominio de Zonalia en POO (#20).

Son clases de Python puro: no saben nada de PostgreSQL ni de la API. Por eso se prueban
sin base de datos y la misma regla vale en la API, en el importador y en el generador.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import date, datetime

from zonalia.dominio.errores import (
    DireccionInvalidaError,
    RepartidorSaturadoError,
    TransicionInvalidaError,
)

# Cambios de estado permitidos. Es la misma tabla que valida el trigger del #11 en la base.
TRANSICIONES: dict[str, set[str]] = {
    "recibido": {"asignado"},
    "asignado": {"en_ruta", "recibido"},
    "en_ruta": {"entregado", "fallido"},
    "fallido": {"asignado", "devuelto"},
    "entregado": set(),
    "devuelto": set(),
}


@dataclass(frozen=True)
class Zona:
    zona_id: int
    nombre: str
    activa: bool = True


@dataclass(frozen=True)
class Colonia:
    colonia_id: int
    codigo_postal: str
    nombre: str
    tipo_asentamiento: str
    zona_id: int

    def __post_init__(self) -> None:
        if not (len(self.codigo_postal) == 5 and self.codigo_postal.isdigit()):
            raise DireccionInvalidaError(f"Código postal inválido: {self.codigo_postal!r}")


@dataclass
class Paquete:
    paquete_id: int
    zona_id: int
    colonia_id: int
    guia: str
    estado: str = "recibido"

    def cambiar_estado(self, nuevo: str) -> None:
        """Cambia el estado solo si la transición está permitida."""
        if nuevo not in TRANSICIONES.get(self.estado, set()):
            raise TransicionInvalidaError(
                f"El paquete {self.guia} no puede pasar de {self.estado} a {nuevo}"
            )
        self.estado = nuevo

    @property
    def asignable(self) -> bool:
        return "asignado" in TRANSICIONES[self.estado]


class Usuario(ABC):
    """Base de los tres roles. Cada rol dice qué puede hacer."""

    rol: str = ""

    def __init__(self, usuario_id: int, nombre_usuario: str, nombre_completo: str) -> None:
        self.usuario_id = usuario_id
        self.nombre_usuario = nombre_usuario
        self.nombre_completo = nombre_completo

    @abstractmethod
    def puede_asignar(self) -> bool:
        """Si el rol puede asignar paquetes a repartidores."""

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.nombre_usuario!r})"


class Administrador(Usuario):
    rol = "admin"

    def puede_asignar(self) -> bool:
        return True


class Supervisor(Usuario):
    rol = "supervisor"

    def puede_asignar(self) -> bool:
        return True


class Repartidor(Usuario):
    rol = "repartidor"

    def __init__(
        self,
        usuario_id: int,
        nombre_usuario: str,
        nombre_completo: str,
        zona_id: int,
        capacidad_diaria: int = 60,
    ) -> None:
        super().__init__(usuario_id, nombre_usuario, nombre_completo)
        self.zona_id = zona_id
        self.capacidad_diaria = capacidad_diaria

    def puede_asignar(self) -> bool:
        return False


@dataclass
class Ruta:
    """Paquetes de un repartidor en un día, en orden de entrega."""

    repartidor: Repartidor
    fecha: date
    paquetes: list[Paquete] = field(default_factory=list)

    @property
    def carga(self) -> int:
        return len(self.paquetes)

    def agregar(self, paquete: Paquete) -> None:
        """Agrega el paquete al final y lo marca como asignado."""
        if paquete.zona_id != self.repartidor.zona_id:
            raise TransicionInvalidaError(
                f"El paquete {paquete.guia} es de la zona {paquete.zona_id} y el repartidor "
                f"de la zona {self.repartidor.zona_id}"
            )
        if self.carga >= self.repartidor.capacidad_diaria:
            raise RepartidorSaturadoError(
                f"{self.repartidor.nombre_usuario} ya tiene {self.carga} paquetes"
            )
        paquete.cambiar_estado("asignado")
        self.paquetes.append(paquete)


@dataclass(frozen=True)
class Entrega:
    paquete: Paquete
    resultado: str
    registrada_en: datetime
    motivo_fallo: str | None = None

    def __post_init__(self) -> None:
        if self.resultado not in ("entregado", "fallido"):
            raise TransicionInvalidaError(f"Resultado desconocido: {self.resultado}")
        if self.resultado == "fallido" and not self.motivo_fallo:
            raise TransicionInvalidaError("Una entrega fallida necesita su motivo")


def usuario_desde_rol(
    rol: str, usuario_id: int, nombre_usuario: str, nombre_completo: str
) -> Usuario:
    """Crea el objeto del rol correcto (para repartidor usa la clase Repartidor directo)."""
    clases: dict[str, type[Usuario]] = {"admin": Administrador, "supervisor": Supervisor}
    if rol not in clases:
        raise ValueError(f"Rol sin clase simple: {rol}")
    return clases[rol](usuario_id, nombre_usuario, nombre_completo)
