"""Shared service for attendance workflows."""

from __future__ import annotations

from datetime import date
from typing import Dict, List, Optional

from app.models.asistencia import Asistencia
from app.models.dbbroker import DBBroker


class AsistenciaService:
    def __init__(self, broker: Optional[DBBroker] = None) -> None:
        self.broker = broker or DBBroker()

    def registrarAsistencia(self, usuario_id: str, rol: str, presente: bool, fecha_registro: Optional[str] = None) -> Asistencia:
        registro = Asistencia(
            id=None,
            usuario_id=usuario_id,
            fecha=fecha_registro or date.today().isoformat(),
            presente=presente,
            rol=rol,
        )
        self.broker.guardarObjeto(registro)
        return registro

    def consultarAsistencia(self, usuario_id: str, rol: str) -> Dict[str, object]:
        registros = [
            Asistencia.from_dict(item)
            for item in self.broker.listar("Asistencia")
            if item.get("usuario_id") == usuario_id and item.get("rol") == rol
        ]
        resumen = self._resumen(registros)
        return {"registros": registros, "resumen": resumen}

    def _resumen(self, registros: List[Asistencia]) -> Dict[str, float]:
        total = len(registros)
        presentes = len([r for r in registros if r.presente])
        porcentaje = Asistencia.CalcularPorcentaje({"total": total, "present": presentes})
        return {"total": float(total), "presentes": float(presentes), "porcentaje": porcentaje}
