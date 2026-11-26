"""Contraseñas con argon2, tokens JWT y permisos por rol."""

from collections.abc import Callable
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import Annotated

import jwt
from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerificationError
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from zonalia.api.config import obtener_config

ROLES = ("admin", "supervisor", "repartidor")
_hasher = PasswordHasher()
_esquema_bearer = HTTPBearer(auto_error=False)


@dataclass(frozen=True)
class UsuarioActual:
    usuario_id: int
    nombre_usuario: str
    rol: str


def hashear_contrasena(contrasena: str) -> str:
    """Devuelve el hash argon2. Es lo único que se guarda; la contraseña nunca."""
    return _hasher.hash(contrasena)


def verificar_contrasena(hash_guardado: str, contrasena: str) -> bool:
    try:
        return _hasher.verify(hash_guardado, contrasena)
    except (VerificationError, InvalidHashError):
        return False


# Hash de relleno: si el usuario no existe se verifica contra él, así la respuesta
# tarda lo mismo y no revela qué usuarios existen.
_HASH_RELLENO = _hasher.hash("contrasena-de-relleno")


def verificar_relleno(contrasena: str) -> None:
    verificar_contrasena(_HASH_RELLENO, contrasena)


def crear_token(usuario_id: int, nombre_usuario: str, rol: str) -> str:
    config = obtener_config()
    ahora = datetime.now(UTC)
    datos = {
        "sub": str(usuario_id),
        "nombre": nombre_usuario,
        "rol": rol,
        "iat": ahora,
        "exp": ahora + timedelta(minutes=config.jwt_minutos_expiracion),
    }
    return jwt.encode(datos, config.jwt_secreto, algorithm="HS256")


def _no_autenticado(detalle: str) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detalle,
        headers={"WWW-Authenticate": "Bearer"},
    )


def usuario_actual(
    request: Request,
    credenciales: Annotated[HTTPAuthorizationCredentials | None, Depends(_esquema_bearer)],
) -> UsuarioActual:
    """Dependencia: exige un token válido y deja al usuario en request.state (lo usa el #16)."""
    if credenciales is None:
        raise _no_autenticado("Falta el token")
    try:
        datos = jwt.decode(
            credenciales.credentials,
            obtener_config().jwt_secreto,
            algorithms=["HS256"],
            options={"require": ["exp", "sub", "rol"]},
        )
    except jwt.ExpiredSignatureError as error:
        raise _no_autenticado("El token expiró") from error
    except jwt.InvalidTokenError as error:
        raise _no_autenticado("Token inválido") from error
    usuario = UsuarioActual(int(datos["sub"]), datos.get("nombre", ""), datos["rol"])
    request.state.usuario = usuario
    return usuario


def requiere_rol(*roles: str) -> Callable[..., UsuarioActual]:
    """Dependencia que deja pasar solo a los roles indicados; a los demás les da 403."""

    def revisar(usuario: Annotated[UsuarioActual, Depends(usuario_actual)]) -> UsuarioActual:
        if usuario.rol not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Tu rol no tiene permiso para esta acción",
            )
        return usuario

    return revisar


if __name__ == "__main__":
    # Genera el hash de una contraseña para dar de alta un usuario a mano:
    #   python -m zonalia.api.seguridad
    # La contraseña se pide sin mostrarla en pantalla y nunca se guarda.
    from getpass import getpass

    print(hashear_contrasena(getpass("Contraseña: ")))
