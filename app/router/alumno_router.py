"""Alumno endpoints covering CU-008 to CU-012."""

from __future__ import annotations

from typing import List

from fastapi import APIRouter, Form, HTTPException, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse

from app.controllers.alumno_service import AlumnoService
from app.controllers.asistencia_service import AsistenciaService
from app.utils.auth import get_current_user
from app.utils.navigation import menu_for_role

router = APIRouter(prefix="/alumno", tags=["Alumno"])
service = AlumnoService()
asistencia_service = AsistenciaService()


def _require_alumno(request: Request):
    usuario = get_current_user(request)
    if usuario.rol != "alumno":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acceso restringido")
    return usuario


@router.get("/inscribirse_materia", response_class=HTMLResponse)
async def inscribirse_materia_view(request: Request) -> HTMLResponse:
    alumno = _require_alumno(request)
    templates = request.app.state.templates
    materias = service.listarMaterias()
    return templates.TemplateResponse(
        "alumno/inscribirse_materia.html",
        {
            "request": request,
            "usuario": alumno,
            "materias": materias,
            "nav_items": menu_for_role(alumno.rol),
            "page_title": "Inscripcion a materias",
        },
    )


@router.post("/inscribirse_materia")
async def inscribirse_materia_action(
    request: Request, materia_id: str = Form(...)
) -> RedirectResponse:
    alumno = _require_alumno(request)
    service.inscribirseMateria(alumno, materia_id)
    return RedirectResponse(
        request.url_for("dashboard"),
        status_code=status.HTTP_303_SEE_OTHER,
    )


@router.get("/inscribirse_examen", response_class=HTMLResponse)
async def inscribirse_examen_view(request: Request) -> HTMLResponse:
    alumno = _require_alumno(request)
    templates = request.app.state.templates
    examenes = service.listarExamenes()
    materias = {materia.id: materia.nombre for materia in service.listarMaterias()}
    return templates.TemplateResponse(
        "alumno/inscribirse_examen.html",
        {
            "request": request,
            "usuario": alumno,
            "examenes": examenes,
            "materias": materias,
            "nav_items": menu_for_role(alumno.rol),
            "page_title": "Inscripcion a examenes",
        },
    )


@router.post("/inscribirse_examen")
async def inscribirse_examen_action(
    request: Request,
    examen_id: str = Form(...),
) -> RedirectResponse:
    alumno = _require_alumno(request)
    service.inscribirseExamen(alumno, examen_id)
    return RedirectResponse(
        request.url_for("dashboard"),
        status_code=status.HTTP_303_SEE_OTHER,
    )


@router.get("/asistencia", response_class=HTMLResponse, name="alumno_asistencia_view")
async def asistencia_view(request: Request) -> HTMLResponse:
    alumno = _require_alumno(request)
    templates = request.app.state.templates
    asistencia = asistencia_service.consultarAsistencia(alumno.id, alumno.rol)  # type: ignore[arg-type]
    return templates.TemplateResponse(
        "alumno/asistencia.html",
        {
            "request": request,
            "usuario": alumno,
            "registros": asistencia["registros"],
            "resumen": asistencia["resumen"],
            "action_url": request.url_for("alumno_asistencia_action"),
            "nav_items": menu_for_role(alumno.rol),
            "page_title": "Mi asistencia",
        },
    )


@router.post("/asistencia", name="alumno_asistencia_action")
async def asistencia_action(
    request: Request,
    presente: str = Form(...),
) -> RedirectResponse:
    alumno = _require_alumno(request)
    asistencia_service.registrarAsistencia(
        alumno.id,  # type: ignore[arg-type]
        alumno.rol,
        presente == "si",
    )
    return RedirectResponse(
        request.url_for("alumno_asistencia_view"),
        status_code=status.HTTP_303_SEE_OTHER,
    )


@router.get("/notas", response_class=HTMLResponse)
async def notas_view(request: Request) -> HTMLResponse:
    alumno = _require_alumno(request)
    templates = request.app.state.templates
    calificaciones = service.obtenerCalificaciones(alumno.id)  # type: ignore[arg-type]
    materias = {materia.id: materia.nombre for materia in service.listarMaterias()}
    return templates.TemplateResponse(
        "alumno/notas.html",
        {
            "request": request,
            "usuario": alumno,
            "calificaciones": calificaciones,
            "materias": materias,
            "nav_items": menu_for_role(alumno.rol),
            "page_title": "Mis calificaciones",
        },
    )

