"""Capa de servicios para los casos de uso del docente."""

from __future__ import annotations

from datetime import date
from typing import List, Optional

from app.models.calificacion import Calificacion
from app.models.dbbroker import DBBroker
from app.models.USRs import Docente
from app.models.materia import Materia


class DocenteService:
    def __init__(self, broker: Optional[DBBroker] = None) -> None:
        self.broker = broker or DBBroker()

    def listarMateriasAsignadas(self, docente: Docente) -> List[Materia]:
        materias = self.broker.listar("Materia")
        return [
            Materia.from_dict(item)
            for item in materias
            if item.get("id") in docente.materiasAsignadas
        ]

    def cargarCalificaciones(
        self, docente: Docente, alumno_id: str, materia_id: str, nota: float
    ) -> Calificacion:
        registro = Calificacion(
            id=None,
            alumno_id=alumno_id,
            materia_id=materia_id,
            nota=nota,
            fecha=date.today().isoformat(),
        )
        self.broker.guardarObjeto(registro)
        return registro
