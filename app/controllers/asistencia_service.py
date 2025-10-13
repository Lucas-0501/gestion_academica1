"""Shared service for attendance workflows."""

from __future__ import annotations

from datetime import date, datetime, timedelta
from typing import Dict, List, Optional, Tuple

from app.models.asistencia import Asistencia
from app.models.dbbroker import DBBroker


class AsistenciaService:
    QUARTERS: Dict[str, Dict[str, object]] = {
        "2025Q1": {
            "label": "1° Cuatrimestre 2025",
            "start": date(2025, 3, 10),
            "end": date(2025, 6, 13),
        },
        "2025Q2": {
            "label": "2° Cuatrimestre 2025",
            "start": date(2025, 7, 28),
            "end": date(2025, 11, 7),
        },
    }

    def __init__(self, broker: Optional[DBBroker] = None) -> None:
        self.broker = broker or DBBroker()

    def registrarAsistencia(self, usuario_id: str, rol: str, presente: bool, fecha_registro: Optional[str] = None) -> Asistencia:
        fecha = fecha_registro or date.today().isoformat()
        if self._existe_asistencia(usuario_id, rol, fecha):
            raise ValueError("Asistencia ya registrada para hoy")
        registro = Asistencia(
            id=None,
            usuario_id=usuario_id,
            fecha=fecha,
            presente=presente,
            rol=rol,
        )
        self.broker.guardarObjeto(registro)
        return registro

    def consultarAsistencia(self, usuario_id: str, rol: str, cuatrimestre: Optional[str] = None) -> Dict[str, object]:
        registros = [
            Asistencia.from_dict(item)
            for item in self.broker.listar("Asistencia")
            if item.get("usuario_id") == usuario_id and item.get("rol") == rol
        ]
        quarter_info = self.QUARTERS.get(cuatrimestre) if cuatrimestre else None
        filtered_registros = registros
        expected_total = len(registros)
        if quarter_info:
            start: date = quarter_info["start"]  # type: ignore[assignment]
            end: date = quarter_info["end"]  # type: ignore[assignment]
            today = date.today()
            if today < start:
                filtered_registros = []
                expected_total = 0
            else:
                effective_end = min(end, today)
                filtered_registros = [
                    registro
                    for registro in registros
                    if start <= datetime.fromisoformat(registro.fecha).date() <= effective_end
                ]
                expected_total = self._count_weekdays(start, effective_end)
        resumen = self._resumen(filtered_registros, expected_total)
        return {
            "registros": filtered_registros,
            "resumen": resumen,
            "quarter": cuatrimestre,
        }

    def listarCuatrimestres(self) -> List[Tuple[str, str]]:
        return [(codigo, data["label"]) for codigo, data in self.QUARTERS.items()]

    def _resumen(self, registros: List[Asistencia], esperado: int) -> Dict[str, float]:
        presentes = len([r for r in registros if r.presente])
        porcentaje = Asistencia.CalcularPorcentaje({"total": esperado, "present": presentes})
        return {"total": float(esperado), "presentes": float(presentes), "porcentaje": porcentaje}

    def _existe_asistencia(self, usuario_id: str, rol: str, fecha: str) -> bool:
        return any(
            item.get("usuario_id") == usuario_id and item.get("rol") == rol and item.get("fecha") == fecha
            for item in self.broker.listar("Asistencia")
        )

    def _count_weekdays(self, start: date, end: date) -> int:
        if end < start:
            return 0
        total_days = (end - start).days + 1
        weekdays = 0
        for i in range(total_days):
            current = start + timedelta(days=i)
            if current.weekday() < 5:
                weekdays += 1
        return weekdays
