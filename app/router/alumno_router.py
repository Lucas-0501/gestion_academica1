"""Endpoints de alumno que cubren los CU-008 al CU-012."""

from __future__ import annotations

from datetime import date
from typing import List
from urllib.parse import quote

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
    materias = service.listarMateriasDisponibles(alumno)
    plan = service.obtenerPlanDelAlumno(alumno)
    materias_inscriptas = service.listarMateriasInscriptas(alumno)
    success = request.query_params.get("success")
    error = request.query_params.get("error")
    return templates.TemplateResponse(
        "alumno/inscribirse_materia.html",
        {
            "request": request,
            "usuario": alumno,
            "materias": materias,
            "plan": plan,
            "materias_inscriptas": materias_inscriptas,
            "nav_items": menu_for_role(alumno.rol),
            "page_title": "Inscripcion a materias",
            "success": success,
            "error": error,
        },
    )


@router.post("/inscribirse_materia")
async def inscribirse_materia_action(
    request: Request, materia_id: str = Form(...)
) -> RedirectResponse:
    alumno = _require_alumno(request)
    url = request.url_for("inscribirse_materia_view")
    try:
        service.inscribirseMateria(alumno, materia_id)
    except ValueError:
        return RedirectResponse(
            f"{url}?error={quote('La materia no pertenece a tu cohorte')}",
            status_code=status.HTTP_303_SEE_OTHER,
        )
    return RedirectResponse(
        f"{url}?success={quote('Inscripcion realizada correctamente')}",
        status_code=status.HTTP_303_SEE_OTHER,
    )


@router.get("/inscribirse_examen", response_class=HTMLResponse)
async def inscribirse_examen_view(request: Request) -> HTMLResponse:
    alumno = _require_alumno(request)
    templates = request.app.state.templates
    examenes = service.listarExamenes()
    materias = {
        materia.id: materia
        for materia in service.listarMaterias()
        if materia.id
    }
    cursos = {
        curso.id: curso
        for curso in service.listarCursos()
        if curso.id
    }
    hoy = date.today()
    examenes_detalle = []
    examenes_inscriptos = []
    for examen in examenes:
        materia = materias.get(examen.materia_id)
        correlativas = [
            materias[correlativa_id].nombre
            for correlativa_id in examen.correlativas
            if correlativa_id in materias
        ]
        curso = cursos.get(examen.curso_id)
        detalle = {
            "examen": examen,
            "materia_nombre": materia.nombre if materia else examen.materia_id,
            "correlativas": correlativas,
            "curso_nombre": curso.nombre if curso else None,
        }
        examenes_detalle.append(detalle)
        if examen.id and examen.id in alumno.examenesInscripto:
            try:
                fecha_examen = date.fromisoformat(examen.fecha)
            except ValueError:
                fecha_examen = None
            examenes_inscriptos.append(
                {
                    **detalle,
                    "es_pasado": fecha_examen < hoy if fecha_examen else False,
                }
            )
    return templates.TemplateResponse(
        "alumno/inscribirse_examen.html",
        {
            "request": request,
            "usuario": alumno,
            "examenes_detalle": examenes_detalle,
            "examenes_inscriptos": examenes_inscriptos,
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
    cuatrimestre = request.query_params.get("cuatrimestre") or "2025Q1"
    quarters = asistencia_service.listarCuatrimestres()
    quarters_dict = dict(quarters)
    if cuatrimestre not in quarters_dict:
        cuatrimestre = "2025Q1"
    asistencia = asistencia_service.consultarAsistencia(alumno.id, alumno.rol, cuatrimestre)  # type: ignore[arg-type]
    success = request.query_params.get("success")
    error = request.query_params.get("error")
    return templates.TemplateResponse(
        "alumno/asistencia.html",
        {
            "request": request,
            "usuario": alumno,
            "registros": asistencia["registros"],
            "resumen": asistencia["resumen"],
            "action_url": request.url_for("alumno_asistencia_action"),
            "cuatrimestres": quarters,
            "cuatrimestre": cuatrimestre,
            "cuatrimestre_label": quarters_dict.get(cuatrimestre),
            "success": success,
            "error": error,
            "nav_items": menu_for_role(alumno.rol),
            "page_title": "Mi asistencia",
        },
    )


@router.post("/asistencia", name="alumno_asistencia_action")
async def asistencia_action(
    request: Request,
    cuatrimestre: str = Form("2025Q1"),
) -> RedirectResponse:
    alumno = _require_alumno(request)
    quarters_dict = dict(asistencia_service.listarCuatrimestres())
    if cuatrimestre not in quarters_dict:
        cuatrimestre = "2025Q1"
    url = request.url_for("alumno_asistencia_view")
    try:
        asistencia_service.registrarAsistencia(
            alumno.id,  # type: ignore[arg-type]
            alumno.rol,
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

