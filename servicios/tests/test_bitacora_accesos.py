"""Pruebas de la bitácora de accesos (#16)."""

import json
import logging

import pytest
from fastapi.testclient import TestClient

from zonalia.api.auth import obtener_repositorio_usuarios
from zonalia.api.main import app
from zonalia.api.seguridad import hashear_contrasena
from zonalia.datos.usuarios import UsuarioGuardado

CONTRASENA = "Clave-Secreta-Prueba-9"


class RepositorioFalso:
    def buscar_por_nombre(self, nombre_usuario: str) -> UsuarioGuardado | None:
        if nombre_usuario == "super1":
            return UsuarioGuardado(1, "super1", hashear_contrasena(CONTRASENA), "supervisor", True)
        return None


@pytest.fixture
def cliente() -> TestClient:
    app.dependency_overrides[obtener_repositorio_usuarios] = RepositorioFalso
    yield TestClient(app)
    app.dependency_overrides.clear()


def lineas(caplog: pytest.LogCaptureFixture) -> list[dict[str, object]]:
    return [json.loads(r.getMessage()) for r in caplog.records if r.name == "zonalia.accesos"]


@pytest.fixture(autouse=True)
def capturar(caplog: pytest.LogCaptureFixture) -> None:
    # Activa la propagación para capturar los registros durante las pruebas.
    logging.getLogger("zonalia.accesos").propagate = True
    caplog.set_level(logging.INFO, logger="zonalia.accesos")
    yield
    logging.getLogger("zonalia.accesos").propagate = False


def test_registra_una_peticion_anonima(
    cliente: TestClient, caplog: pytest.LogCaptureFixture
) -> None:
    cliente.get("/health?x=1", headers={"X-Real-IP": "10.10.0.9"})
    (linea,) = lineas(caplog)
    assert linea["evento"] == "peticion"
    assert linea["metodo"] == "GET"
    assert linea["ruta"] == "/health"
    assert linea["ip"] == "10.10.0.9"
    assert linea["codigo"] == 200
    assert linea["usuario"] is None
    assert "hora" in linea


def test_registra_usuario_y_rol_con_token(
    cliente: TestClient, caplog: pytest.LogCaptureFixture
) -> None:
    r = cliente.post("/auth/login", json={"nombre_usuario": "super1", "contrasena": CONTRASENA})
    token = r.json()["access_token"]
    caplog.clear()
    cliente.get("/auth/yo", headers={"Authorization": f"Bearer {token}"})
    (linea,) = lineas(caplog)
    assert linea["usuario"] == "super1"
    assert linea["rol"] == "supervisor"
    assert linea["codigo"] == 200


def test_registra_login_fallido(cliente: TestClient, caplog: pytest.LogCaptureFixture) -> None:
    cliente.post("/auth/login", json={"nombre_usuario": "super1", "contrasena": "equivocada"})
    (linea,) = lineas(caplog)
    assert linea["evento"] == "login_fallido"
    assert linea["usuario_intentado"] == "super1"
    assert linea["codigo"] == 401
    assert caplog.records[-1].levelname == "WARNING"


def test_nunca_guarda_contrasenas_ni_tokens(
    cliente: TestClient, caplog: pytest.LogCaptureFixture
) -> None:
    r = cliente.post("/auth/login", json={"nombre_usuario": "super1", "contrasena": CONTRASENA})
    token = r.json()["access_token"]
    cliente.get("/auth/yo", headers={"Authorization": f"Bearer {token}"})
    cliente.post(
        "/auth/login", json={"nombre_usuario": "super1", "contrasena": "Otra-Clave-Mala-7"}
    )
    texto = "\n".join(r.getMessage() for r in caplog.records)
    assert CONTRASENA not in texto
    assert "Otra-Clave-Mala-7" not in texto
    assert token not in texto
    assert "Bearer" not in texto
