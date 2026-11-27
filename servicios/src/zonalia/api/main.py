"""Punto de entrada de la API REST de Zonalia."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from zonalia.api import auth
from zonalia.api.bitacora_accesos import BitacoraAccesos, configurar_bitacora
from zonalia.api.config import obtener_config

app = FastAPI(title="Zonalia API", version="0.1.0")

# Solo la web publicada puede llamar a la API desde un navegador.
app.add_middleware(
    CORSMiddleware,
    allow_origins=obtener_config().cors_origenes,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)

# Bitácora de accesos de la API (#16).
configurar_bitacora()
app.add_middleware(BitacoraAccesos)

app.include_router(auth.router)


@app.get("/health")
def health() -> dict[str, str]:
    """Indica que la API está viva. Lo usan Docker y el monitoreo de nodos."""
    return {"estado": "ok"}
