"""Pruebas de inicio de sesión, roles y CORS (#13). No necesitan base de datos."""

from typing import Annotated

import jwt
import pytest
from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient

from zonalia.api.auth import obtener_repositorio_usuarios
from zonalia.api.config import obtener_config
from zonalia.api.main import app
from zonalia.api.seguridad import (
    UsuarioActual,
    crear_token,
    hashear_contrasena,
    requiere_rol,
    verificar_contrasena,
)
from zonalia.datos.usuarios import UsuarioGuardado


class RepositorioFalso:
    """Usuarios en memoria, en lugar de PostgreSQL."""

    def __init__(self) -> None:
        self._usuarios = {
            "super1": UsuarioGuardado(
                1, "super1", hashear_contrasena("Clave-Prueba-1"), "supervisor", True
            ),
            "baja1": UsuarioGuardado(
                2, "baja1", hashear_contrasena("Clave-Prueba-2"), "repartidor", False
            ),
        }

    def buscar_por_nombre(self, nombre_usuario: str) -> UsuarioGuardado | None:
        return self._usuarios.get(nombre_usuario)


@pytest.fixture
def cliente() -> TestClient:
    app.dependency_overrides[obtener_repositorio_usuarios] = RepositorioFalso
    yield TestClient(app)
    app.dependency_overrides.clear()


def test_hash_no_guarda_la_contrasena() -> None:
    hash_ = hashear_contrasena("Clave-Prueba-1")
    assert "Clave-Prueba-1" not in hash_
    assert hash_.startswith("$argon2id$")
    assert verificar_contrasena(hash_, "Clave-Prueba-1")
    assert not verificar_contrasena(hash_, "otra")


def test_login_correcto_da_token_con_rol(cliente: TestClient) -> None:
    r = cliente.post(
        "/auth/login", json={"nombre_usuario": "super1", "contrasena": "Clave-Prueba-1"}
    )
    assert r.status_code == 200
    token = r.json()["access_token"]
    datos = jwt.decode(token, obtener_config().jwt_secreto, algorithms=["HS256"])
    assert datos["rol"] == "supervisor"
    assert datos["exp"] > datos["iat"]
    yo = cliente.get("/auth/yo", headers={"Authorization": f"Bearer {token}"})
    assert yo.status_code == 200
    assert yo.json()["nombre_usuario"] == "super1"


@pytest.mark.parametrize(
    ("usuario", "contrasena"),
    [("super1", "equivocada"), ("no-existe", "Clave-Prueba-1"), ("baja1", "Clave-Prueba-2")],
)
def test_login_fallido_da_401(cliente: TestClient, usuario: str, contrasena: str) -> None:
    r = cliente.post("/auth/login", json={"nombre_usuario": usuario, "contrasena": contrasena})
    assert r.status_code == 401
    assert r.json()["detail"] == "Usuario o contraseña incorrectos"


def test_sin_token_o_token_falso_da_401(cliente: TestClient) -> None:
    assert cliente.get("/auth/yo").status_code == 401
    r = cliente.get("/auth/yo", headers={"Authorization": "Bearer no-es-un-token"})
    assert r.status_code == 401


def test_token_expirado_da_401(cliente: TestClient, monkeypatch: pytest.MonkeyPatch) -> None:
    config = obtener_config()
    monkeypatch.setattr(
        "zonalia.api.seguridad.obtener_config",
        lambda: type(config)(config.jwt_secreto, -1, config.cors_origenes),
    )
    token = crear_token(1, "super1", "supervisor")
    monkeypatch.undo()
    r = cliente.get("/auth/yo", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 401
    assert r.json()["detail"] == "El token expiró"


def test_rol_sin_permiso_da_403() -> None:
    app_prueba = FastAPI()

    @app_prueba.get("/solo-admin")
    def solo_admin(
        usuario: Annotated[UsuarioActual, Depends(requiere_rol("admin"))],
    ) -> dict[str, str]:
        return {"hola": usuario.nombre_usuario}

    cliente = TestClient(app_prueba)
    token_supervisor = crear_token(1, "super1", "supervisor")
    token_admin = crear_token(3, "admin1", "admin")
    r = cliente.get("/solo-admin", headers={"Authorization": f"Bearer {token_supervisor}"})
    assert r.status_code == 403
    r = cliente.get("/solo-admin", headers={"Authorization": f"Bearer {token_admin}"})
    assert r.status_code == 200


def test_cors_solo_permite_la_web(cliente: TestClient) -> None:
    permitido = cliente.options(
        "/auth/login",
        headers={"Origin": "https://zonalia.local", "Access-Control-Request-Method": "POST"},
    )
    assert permitido.headers.get("access-control-allow-origin") == "https://zonalia.local"
    otro = cliente.options(
        "/auth/login",
        headers={"Origin": "https://sitio-ajeno.com", "Access-Control-Request-Method": "POST"},
    )
    assert "access-control-allow-origin" not in otro.headers
