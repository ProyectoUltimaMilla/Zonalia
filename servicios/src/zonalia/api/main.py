"""Punto de entrada de la API REST de Zonalia."""

from fastapi import FastAPI

app = FastAPI(title="Zonalia API", version="0.1.0")


@app.get("/health")
def health() -> dict[str, str]:
    """Indica que la API está viva. Lo usan Docker y el monitoreo de nodos."""
    return {"estado": "ok"}
