"""Rutas de inicio de sesión."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel

from zonalia.api.seguridad import (
    UsuarioActual,
    crear_token,
    usuario_actual,
    verificar_contrasena,
    verificar_relleno,
)
from zonalia.datos.usuarios import (
    RepositorioUsuarios,
    RepositorioUsuariosPostgres,
    conninfo_desde_entorno,
)

router = APIRouter(prefix="/auth", tags=["autenticación"])


class DatosLogin(BaseModel):
    nombre_usuario: str
    contrasena: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    rol: str


def obtener_repositorio_usuarios() -> RepositorioUsuarios:
    return RepositorioUsuariosPostgres(conninfo_desde_entorno())


@router.post("/login")
def login(
    datos: DatosLogin,
    request: Request,
    repositorio: Annotated[RepositorioUsuarios, Depends(obtener_repositorio_usuarios)],
) -> Token:
    """Devuelve un JWT si el usuario existe, está activo y la contraseña coincide."""
    usuario = repositorio.buscar_por_nombre(datos.nombre_usuario)
    if usuario is None:
        verificar_relleno(datos.contrasena)
    correcto = (
        usuario is not None
        and usuario.activo
        and verificar_contrasena(usuario.hash_contrasena, datos.contrasena)
    )
    if not correcto:
        # El #16 registra este intento fallido en la bitácora de accesos.
        request.state.login_fallido = datos.nombre_usuario
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
        )
    token = crear_token(usuario.usuario_id, usuario.nombre_usuario, usuario.rol)
    return Token(access_token=token, rol=usuario.rol)


@router.get("/yo")
def yo(usuario: Annotated[UsuarioActual, Depends(usuario_actual)]) -> dict[str, str | int]:
    """Datos del usuario del token. La app lo usa para saber qué pantallas mostrar."""
    return {
        "usuario_id": usuario.usuario_id,
        "nombre_usuario": usuario.nombre_usuario,
        "rol": usuario.rol,
    }
