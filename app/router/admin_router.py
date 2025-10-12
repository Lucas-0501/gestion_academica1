"""Administrador endpoints covering CU-002 to CU-007."""

from __future__ import annotations

from typing import List

from fastapi import APIRouter, Form, HTTPException, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse

from app.controllers.administrador_service import AdministradorService
from app.utils.auth import get_current_user
from app.utils.navigation import menu_for_role

router = APIRouter(prefix="/admin", tags=["Administrador"])
service = AdministradorService()


def _require_admin(request: Request):
    usuario = get_current_user(request)
    if usuario.rol != "administrador":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acceso restringido")
    return usuario


@router.get("/registrar_usuario", response_class=HTMLResponse)
async def registrar_usuario_view(request: Request) -> HTMLResponse:
    admin = _require_admin(request)
    templates = request.app.state.templates
    return templates.TemplateResponse(
        "admin/registrar_usuario.html",
        {
            "request": request,
            "usuario": admin,
            "nav_items": menu_for_role(admin.rol),
            "page_title": "Registrar usuarios",
        },
    )


@router.post("/registrar_usuario")
async def registrar_usuario_action(
    request: Request,
    nombre: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    tipo: str = Form(...),
) -> RedirectResponse:
    _require_admin(request)
    if tipo == "alumno":
        service.registrarAlumno(nombre, email, password)
    elif tipo == "docente":
        service.registrarDocente(nombre, email, password)
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tipo invalido")
    return RedirectResponse(
        request.url_for("dashboard"),
        status_code=status.HTTP_303_SEE_OTHER,
    )


@router.get("/crear_materia", response_class=HTMLResponse)
async def crear_materia_view(request: Request) -> HTMLResponse:
    admin = _require_admin(request)
    templates = request.app.state.templates
    return templates.TemplateResponse(
        "admin/crear_materia.html",
        {
            "request": request,
            "usuario": admin,
            "nav_items": menu_for_role(admin.rol),
            "page_title": "Crear materia",
        },
    )


@router.post("/crear_materia")
async def crear_materia_action(
    request: Request,
    nombre: str = Form(...),
    codigo: str = Form(...),
    descripcion: str = Form(""),
) -> RedirectResponse:
    admin = _require_admin(request)
    service.crearMateria(admin, nombre, codigo, descripcion)
    return RedirectResponse(
        request.url_for("dashboard"),
        status_code=status.HTTP_303_SEE_OTHER,
    )


@router.get("/crear_plan", response_class=HTMLResponse)
async def crear_plan_view(request: Request) -> HTMLResponse:
    admin = _require_admin(request)
    templates = request.app.state.templates
    return templates.TemplateResponse(
        "admin/crear_plan.html",
        {
            "request": request,
            "usuario": admin,
            "nav_items": menu_for_role(admin.rol),
            "page_title": "Crear plan",
        },
    )


@router.post("/crear_plan")
async def crear_plan_action(
    request: Request,
    nombre: str = Form(...),
    descripcion: str = Form(""),
) -> RedirectResponse:
    admin = _require_admin(request)
    service.crearPlan(admin, nombre, descripcion)
    return RedirectResponse(
        request.url_for("dashboard"),
        status_code=status.HTTP_303_SEE_OTHER,
    )


@router.get("/asignar_materia_plan", response_class=HTMLResponse)
async def asignar_materia_plan_view(request: Request) -> HTMLResponse:
    admin = _require_admin(request)
    templates = request.app.state.templates
    planes = service.listarPlanes()
    materias = service.listarMaterias()
    return templates.TemplateResponse(
        "admin/asignar_materia_plan.html",
        {
            "request": request,
            "planes": planes,
            "materias": materias,
            "usuario": admin,
            "nav_items": menu_for_role(admin.rol),
            "page_title": "Asignar materias a plan",
        },
    )


@router.post("/asignar_materia_plan")
async def asignar_materia_plan_action(
    request: Request,
    plan_id: str = Form(...),
    materias_ids: List[str] = Form(default=[]),
) -> RedirectResponse:
    _require_admin(request)
    service.asignarMateriasAPlan(plan_id, materias_ids)
    return RedirectResponse(
        request.url_for("dashboard"),
        status_code=status.HTTP_303_SEE_OTHER,
    )


@router.get("/crear_cohorte", response_class=HTMLResponse)
async def crear_cohorte_view(request: Request) -> HTMLResponse:
    admin = _require_admin(request)
    templates = request.app.state.templates
    planes = service.listarPlanes()
    alumnos = service.listarAlumnos()
    return templates.TemplateResponse(
        "admin/crear_cohorte.html",
        {
            "request": request,
            "planes": planes,
            "alumnos": alumnos,
            "usuario": admin,
            "nav_items": menu_for_role(admin.rol),
            "page_title": "Crear cohorte",
        },
    )


@router.post("/crear_cohorte")
async def crear_cohorte_action(
    request: Request,
    nombre: str = Form(...),
    plan_id: str = Form(...),
    alumnos_ids: List[str] = Form(default=[]),
) -> RedirectResponse:
    admin = _require_admin(request)
    service.crearCohorte(admin, nombre, plan_id, alumnos_ids or None)
    return RedirectResponse(
        request.url_for("dashboard"),
        status_code=status.HTTP_303_SEE_OTHER,
    )


@router.get("/crear_curso", response_class=HTMLResponse)
async def crear_curso_view(request: Request) -> HTMLResponse:
    admin = _require_admin(request)
    templates = request.app.state.templates
    materias = service.listarMaterias()
    cohortes = service.listarCohortes()
    docentes = service.listarDocentes()
    return templates.TemplateResponse(
        "admin/crear_curso.html",
        {
            "request": request,
            "materias": materias,
            "cohortes": cohortes,
            "docentes": docentes,
            "usuario": admin,
            "nav_items": menu_for_role(admin.rol),
            "page_title": "Crear curso",
        },
    )


@router.post("/crear_curso")
async def crear_curso_action(
    request: Request,
    nombre: str = Form(...),
    materia_id: str = Form(...),
    cohorte_id: str = Form(None),
    docente_id: str = Form(None),
) -> RedirectResponse:
    admin = _require_admin(request)
    service.crearCurso(
        admin,
        nombre,
        materia_id,
        cohorte_id or None,
        docente_id or None,
    )
    return RedirectResponse(
        request.url_for("dashboard"),
        status_code=status.HTTP_303_SEE_OTHER,
    )
