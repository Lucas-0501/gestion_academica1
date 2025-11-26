"""Endpoints de autenticacion y panel compartido."""

from __future__ import annotations

import re
from typing import Dict
from urllib.parse import quote

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette import status

from app.controllers.alumno_service import AlumnoService
from app.controllers.auth_service import AuthService
from app.models.USRs import Alumno
from app.models.cohorte import Cohorte
from app.models.dbbroker import DBBroker
from app.utils.auth import get_current_user, login_user, logout_user
from app.utils.navigation import menu_for_role

router = APIRouter()
_USUARIO_REGEX = re.compile(r"^[A-Za-z0-9@._-]+$")


def _redirect_login(request: Request, error: str) -> RedirectResponse:
    url = request.url_for("login_view")
    return RedirectResponse(
        f"{url}?error={quote(error)}",
        status_code=status.HTTP_303_SEE_OTHER,
    )


def _validar_usuario(usuario: str) -> str | None:
    if not usuario:
        return "El campo usuario es obligatorio"
    if len(usuario) < 3:
        return "Usuario debe tener minimo 3 caracteres"
    if len(usuario) > 40:
        return "Usuario maximo 40 caracteres"
    if not _USUARIO_REGEX.match(usuario):
        return "Usuario solo puede contener letras y numeros"
    return None


def _validar_password(password: str) -> str | None:
    if not password:
        return "El campo contraseña es obligatorio"
    if not any(char.isdigit() for char in password):
        return "La contraseña debe contener al menos 1 número"
    return None
   


@router.get("/", response_class=HTMLResponse)
async def login_view(request: Request, error: str | None = None) -> HTMLResponse:
    templates = request.app.state.templates
    return templates.TemplateResponse(
        "login.html",
        {
            "request": request,
            "error": error,
            "nav_items": [],
            "page_title": "Iniciar sesion",
            "is_auth_page": True,
        },
    )


@router.post("/auth/login")
async def login_action(
    request: Request,
    usuario: str = Form(""),
    password: str = Form(""),
) -> RedirectResponse:
    usuario = usuario.strip()
    password = password.strip()

    error_msg = _validar_usuario(usuario)
    if error_msg:
        return _redirect_login(request, error_msg)

    password_error = _validar_password(password)
    if password_error:
        return _redirect_login(request, password_error)

    auth_service = AuthService()
    try:
        usuario_obj = auth_service.iniciarSesion(usuario, password)
    except ValueError as exc:
        return _redirect_login(request, str(exc))

    login_user(request, usuario_obj.to_dict())
    return RedirectResponse(
        request.url_for("dashboard"),
        status_code=status.HTTP_303_SEE_OTHER,
    )


@router.get("/auth/logout")
async def logout_action(request: Request) -> RedirectResponse:
    logout_user(request)
    return RedirectResponse(
        request.url_for("login_view"),
        status_code=status.HTTP_303_SEE_OTHER,
    )


@router.get("/dashboard", response_class=HTMLResponse, name="dashboard")
async def dashboard(request: Request) -> HTMLResponse:
    usuario = get_current_user(request)
    templates = request.app.state.templates
    plan_actual = None
    cohorte_actual = None
    if isinstance(usuario, Alumno):
        alumno_service = AlumnoService()
        plan_actual = alumno_service.obtenerPlanDelAlumno(usuario)
        if usuario.cohorte_id:
            broker = DBBroker()
            cohorte_data = broker.obtenerPorId("Cohorte", usuario.cohorte_id)
            if cohorte_data:
                cohorte_actual = Cohorte.from_dict(cohorte_data)
    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "usuario": usuario,
            "nav_items": menu_for_role(usuario.rol),
            "page_title": "Panel principal",
            "subtitle": "Acciones rapidas para tu rol",
            "plan_actual": plan_actual,
            "cohorte_actual": cohorte_actual,
        },
    )