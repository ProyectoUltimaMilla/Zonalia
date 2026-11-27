"""Clasificador: dice a qué zona va un paquete según su colonia y código postal (#20)."""

import unicodedata

from zonalia.dominio.errores import DireccionInvalidaError, ZonaNoEncontradaError
from zonalia.dominio.modelos import Colonia


def normalizar(texto: str) -> str:
    """Minúsculas, sin acentos y sin espacios de más: 'Río  Bravo' -> 'rio bravo'."""
    sin_acentos = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    return " ".join(sin_acentos.lower().split())


class Clasificador:
    """Conoce el catálogo de colonias y resuelve la zona de una dirección."""

    def __init__(self, colonias: list[Colonia]) -> None:
        self._por_cp_y_nombre: dict[tuple[str, str], Colonia] = {}
        self._zonas_por_cp: dict[str, set[int]] = {}
        for colonia in colonias:
            self._por_cp_y_nombre[(colonia.codigo_postal, normalizar(colonia.nombre))] = colonia
            self._zonas_por_cp.setdefault(colonia.codigo_postal, set()).add(colonia.zona_id)

    def colonia(self, codigo_postal: str, nombre_colonia: str) -> Colonia:
        """Busca la colonia exacta. Si el CP no existe o la colonia no está en él, falla."""
        codigo_postal = codigo_postal.strip()
        if not (len(codigo_postal) == 5 and codigo_postal.isdigit()):
            raise DireccionInvalidaError(f"Código postal inválido: {codigo_postal!r}")
        if not nombre_colonia.strip():
            raise DireccionInvalidaError("Falta la colonia")
        encontrada = self._por_cp_y_nombre.get((codigo_postal, normalizar(nombre_colonia)))
        if encontrada is None:
            raise ZonaNoEncontradaError(
                f"La colonia {nombre_colonia!r} no está en el CP {codigo_postal}"
            )
        return encontrada

    def zona(self, codigo_postal: str, nombre_colonia: str) -> int:
        """Zona de la dirección. Usa la colonia; la zona sale del catálogo del #9."""
        return self.colonia(codigo_postal, nombre_colonia).zona_id

    def zona_por_cp(self, codigo_postal: str) -> int:
        """Zona solo con el CP. Todas las colonias de un CP están en la misma zona (#9)."""
        zonas = self._zonas_por_cp.get(codigo_postal.strip())
        if not zonas:
            raise ZonaNoEncontradaError(f"El CP {codigo_postal} no está en el catálogo")
        return min(zonas)
