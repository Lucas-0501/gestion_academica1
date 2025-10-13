"""Capa de servicios para los casos de uso del alumno."""

from __future__ import annotations

from typing import List, Optional, Set

from app.models.USRs import Alumno
from app.models.calificacion import Calificacion
from app.models.dbbroker import DBBroker
from app.models.examen import Examen
from app.models.materia import Materia
from app.models.plan import Plan


class AlumnoService:
    def __init__(self, broker: Optional[DBBroker] = None) -> None:
        self.broker = broker or DBBroker()

    def listarMaterias(self) -> List[Materia]:
        return [Materia.from_dict(item) for item in self.broker.listar("Materia")]

    def obtenerPlanDelAlumno(self, alumno: Alumno) -> Optional[Plan]:
        if not alumno.plan_id:
            return None
        data = self.broker.obtenerPorId("Plan", alumno.plan_id)
        if not data:
            return None
        return Plan.from_dict(data)

    def listarMateriasDisponibles(self, alumno: Alumno) -> List[Materia]:
        plan = self.obtenerPlanDelAlumno(alumno)
        if not plan:
            return []
        materias_dict = {
            materia.id: materia for materia in self.listarMaterias()
        }
        return [
            materias_dict[materia_id]
            for materia_id in plan.materias
            if materia_id in materias_dict
        ]

    def listarExamenes(self) -> List[Examen]:
        return [Examen.from_dict(item) for item in self.broker.listar("Examen")]

    def inscribirseMateria(self, alumno: Alumno, materia_id: str) -> Alumno:
        disponibles: Set[str] = {materia.id for materia in self.listarMateriasDisponibles(alumno)}
        if materia_id not in disponibles:
            raise ValueError("Materia no permitida para este alumno")
        alumno.inscribirseMateria(materia_id)
        self.broker.actualizarObjeto(alumno)
        return alumno

    def inscribirseExamen(self, alumno: Alumno, examen_id: str) -> Alumno:
        alumno.inscribirseExamen(examen_id)
        self.broker.actualizarObjeto(alumno)
        return alumno

    def obtenerCalificaciones(self, alumno_id: str) -> List[Calificacion]:
        registros = [
            item for item in self.broker.listar("Calificacion") if item.get("alumno_id") == alumno_id
        ]
        return [Calificacion.from_dict(item) for item in registros]
