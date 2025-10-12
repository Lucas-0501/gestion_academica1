"""Session helper utilities."""

from __future__ import annotations

from typing import Any, Dict, Optional

from fastapi import HTTPException, Request, status

from app.models.dbbroker import DBBroker
from app.models.usuario import Usuario
from app.models.alumno import Alumno
from app.models.docente import Docente
from app.models.administrador import Administrador


SESSION_USER_KEY = "sesion_usuario_id"


def _build_usuario(data: Dict[str, Any]) -> Usuario:
    tipo = data.get("type") or data.get("rol", "").capitalize()
    if tipo == "Alumno":
        return Alumno.from_dict(data)
    if tipo == "Docente":
        return Docente.from_dict(data)
    if tipo == "Administrador":
        return Administrador.from_dict(data)
    return Usuario.from_dict(data)


def login_user(request: Request, user_data: Dict[str, Any]) -> None:
    request.session[SESSION_USER_KEY] = user_data["id"]


def logout_user(request: Request) -> None:
    request.session.pop(SESSION_USER_KEY, None)


def get_current_user(request: Request) -> Usuario:
    user_id = request.session.get(SESSION_USER_KEY)
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No autenticado")
    broker = DBBroker()
    data = broker.obtenerPorId("Usuario", user_id)
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    return _build_usuario(data)


def get_current_user_optional(request: Request) -> Optional[Usuario]:
    user_id = request.session.get(SESSION_USER_KEY)
    if not user_id:
        return None
    broker = DBBroker()
    data = broker.obtenerPorId("Usuario", user_id)
    return _build_usuario(data) if data else None
