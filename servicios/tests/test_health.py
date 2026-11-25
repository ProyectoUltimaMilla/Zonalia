"""Prueba del endpoint /health."""

from fastapi.testclient import TestClient

from zonalia.api.main import app

cliente = TestClient(app)


def test_health_responde_ok() -> None:
    respuesta = cliente.get("/health")
    assert respuesta.status_code == 200
    assert respuesta.json() == {"estado": "ok"}
