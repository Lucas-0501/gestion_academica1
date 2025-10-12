"""Service layer for alumno use cases."""

from __future__ import annotations

from typing import List, Optional

from app.models.alumno import Alumno
from app.models.calificacion import Calificacion
from app.models.dbbroker import DBBroker
from app.models.examen import Examen
from app.models.materia import Materia


class AlumnoService:
    def __init__(self, broker: Optional[DBBroker] = None) -> None:
        self.broker = broker or DBBroker()

    def listarMaterias(self) -> List[Materia]:
        return [Materia.from_dict(item) for item in self.broker.listar("Materia")]

    def listarExamenes(self) -> List[Examen]:
        return [Examen.from_dict(item) for item in self.broker.listar("Examen")]

    def inscribirseMateria(self, alumno: Alumno, materia_id: str) -> Alumno:
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
