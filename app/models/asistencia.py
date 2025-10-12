"""Asistencia domain model."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class Asistencia:
    id: Optional[str]
    usuario_id: str
    fecha: str
    presente: bool
    rol: str

    def to_dict(self) -> Dict[str, object]:
        return {
            "id": self.id,
            "usuario_id": self.usuario_id,
            "fecha": self.fecha,
            "presente": self.presente,
            "rol": self.rol,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, object]) -> "Asistencia":
        return cls(
            id=data.get("id"),  # type: ignore[arg-type]
            usuario_id=data["usuario_id"],  # type: ignore[index]
            fecha=data["fecha"],  # type: ignore[index]
            presente=bool(data.get("presente", False)),
            rol=data["rol"],  # type: ignore[index]
        )

    @staticmethod
    def CalcularPorcentaje(records: Dict[str, int]) -> float:
        total = records.get("total", 0)
        present = records.get("present", 0)
        if total == 0:
            return 0.0
        return round((present / total) * 100, 2)
