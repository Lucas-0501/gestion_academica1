"""Endpoints de docente que cubren los CU-013 al CU-016."""

from __future__ import annotations

from typing import List
from urllib.parse import quote

from fastapi import APIRouter, Form, HTTPException, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse

from app.controllers.administrador_service import AdministradorService
from app.controllers.asistencia_service import AsistenciaService
from app.controllers.docente_service import DocenteService
from app.utils.auth import get_current_user
from app.utils.navigation import menu_for_role

router = APIRouter(prefix="/docente", tags=["Docente"])
service = DocenteService()
asistencia_service = AsistenciaService()
admin_service = AdministradorService()


def _require_docente(request: Request):
    usuario = get_current_user(request)
    if usuario.rol != "docente":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acceso restringido")
    return usuario


@router.get("/asistencia", response_class=HTMLResponse, name="docente_asistencia_view")
async def asistencia_view(request: Request) -> HTMLResponse:
    docente = _require_docente(request)
    templates = request.app.state.templates
    cuatrimestre = request.query_params.get("cuatrimestre") or "2025Q1"
    quarters = asistencia_service.listarCuatrimestres()
    quarters_dict = dict(quarters)
    if cuatrimestre not in quarters_dict:
        cuatrimestre = "2025Q1"
    asistencia = asistencia_service.consultarAsistencia(docente.id, docente.rol, cuatrimestre)  # type: ignore[arg-type]
    success = request.query_params.get("success")
    error = request.query_params.get("error")
    return templates.TemplateResponse(
        "docente/asistencia.html",
        {
            "request": request,
            "usuario": docente,
            "registros": asistencia["registros"],
            "resumen": asistencia["resumen"],
            "action_url": request.url_for("docente_asistencia_action"),
            "cuatrimestres": quarters,
            "cuatrimestre": cuatrimestre,
            "cuatrimestre_label": quarters_dict.get(cuatrimestre),
            "success": success,
            "error": error,
            "nav_items": menu_for_role(docente.rol),
            "page_title": "Mi asistencia",
        },
    )


@router.post("/asistencia", name="docente_asistencia_action")
async def asistencia_action(
    request: Request,
    cuatrimestre: str = Form("2025Q1"),
) -> RedirectResponse:
    docente = _require_docente(request)
    quarters_dict = dict(asistencia_service.listarCuatrimestres())
    if cuatrimestre not in quarters_dict:
        cuatrimestre = "2025Q1"
    url = request.url_for("docente_asistencia_view")
    try:
        asistencia_service.registrarAsistencia(
            docente.id,  # type: ignore[arg-type]
            docente.rol,
            True,
        )
    except ValueError:
        return RedirectResponse(
            f"{url}?cuatrimestre={cuatrimestre}&error={quote('Ya registraste asistencia para hoy')}",
            status_code=status.HTTP_303_SEE_OTHER,
        )
    return RedirectResponse(
        f"{url}?cuatrimestre={cuatrimestre}&success={quote('Asistencia registrada correctamente')}",
        status_code=status.HTTP_303_SEE_OTHER,
    )


@router.get("/cargar_calificaciones", response_class=HTMLResponse)
async def cargar_calificaciones_view(request: Request) -> HTMLResponse:
    docente = _require_docente(request)
    templates = request.app.state.templates
    materias = service.listarMateriasAsignadas(docente)
    if not materias:
        materias = admin_service.listarMaterias()
    alumnos = admin_service.listarAlumnos()
    return templates.TemplateResponse(
        "docente/cargar_calificaciones.html",
        {
            "request": request,
            "usuario": docente,
            "materias": materias,
            "alumnos": alumnos,
            "nav_items": menu_for_role(docente.rol),
            "page_title": "Cargar calificaciones",
        },
    )


@router.post("/cargar_calificaciones")
async def cargar_calificaciones_action(
    request: Request,
    alumno_id: str = Form(...),
    materia_id: str = Form(...),
    nota: float = Form(...),
) -> RedirectResponse:
    docente = _require_docente(request)
    service.cargarCalificaciones(docente, alumno_id, materia_id, nota)
    return RedirectResponse(
        request.url_for("dashboard"),
        status_code=status.HTTP_303_SEE_OTHER,
    )
