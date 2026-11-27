"""Bitácora de accesos (#16): una línea JSON por cada petición a la API."""

import json
import logging
import os
import time
from datetime import UTC, datetime

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

bitacora = logging.getLogger("zonalia.accesos")


def configurar_bitacora() -> None:
    """Configura la salida de la bitácora."""
    if bitacora.handlers:
        return
    ruta = os.environ.get("BITACORA_ACCESOS_RUTA", "")
    manejador = logging.FileHandler(ruta, encoding="utf-8") if ruta else logging.StreamHandler()
    manejador.setFormatter(logging.Formatter("%(message)s"))
    bitacora.addHandler(manejador)
    bitacora.setLevel(logging.INFO)
    bitacora.propagate = False


def ip_de(request: Request) -> str:
    """Obtiene la IP del cliente detrás de Nginx."""
    return request.headers.get("x-real-ip") or (request.client.host if request.client else "")


def registro(request: Request, codigo: int, inicio: float) -> dict[str, object]:
    usuario = getattr(request.state, "usuario", None)
    datos: dict[str, object] = {
        "hora": datetime.now(UTC).isoformat(timespec="seconds"),
        "evento": "peticion",
        "usuario_id": usuario.usuario_id if usuario else None,
        "usuario": usuario.nombre_usuario if usuario else None,
        "rol": usuario.rol if usuario else None,
        "metodo": request.method,
        "ruta": request.url.path,
        "ip": ip_de(request),
        "codigo": codigo,
        "duracion_ms": round((time.perf_counter() - inicio) * 1000, 1),
    }
    intento = getattr(request.state, "login_fallido", None)
    if intento is not None:
        datos["evento"] = "login_fallido"
        datos["usuario_intentado"] = intento
    return datos


class BitacoraAccesos(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        inicio = time.perf_counter()
        try:
            respuesta = await call_next(request)
        except Exception:
            bitacora.error(json.dumps(registro(request, 500, inicio), ensure_ascii=False))
            raise
        nivel = logging.WARNING if respuesta.status_code in (401, 403) else logging.INFO
        bitacora.log(
            nivel, json.dumps(registro(request, respuesta.status_code, inicio), ensure_ascii=False)
        )
        return respuesta
