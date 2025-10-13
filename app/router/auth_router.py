"""Endpoints de autenticación y panel compartido."""

from __future__ import annotations

from typing import Dict

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette import status

from app.controllers.auth_service import AuthService
from app.utils.auth import get_current_user, login_user, logout_user
from app.utils.navigation import menu_for_role

router = APIRouter()
auth_service = AuthService()


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
    email: str = Form(...),
    password: str = Form(...),
) -> RedirectResponse:
    try:
        usuario = auth_service.iniciarSesion(email, password)
    except ValueError:
        url = request.url_for("login_view")
        return RedirectResponse(
            f"{url}?error=Credenciales%20invalidas",
            status_code=status.HTTP_303_SEE_OTHER,
        )
    login_user(request, usuario.to_dict())
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
    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "usuario": usuario,
            "nav_items": menu_for_role(usuario.rol),
            "page_title": "Panel principal",
            "subtitle": "Acciones rapidas para tu rol",
        },
    )
