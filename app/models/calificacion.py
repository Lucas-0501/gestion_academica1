"""Calificacion domain model."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class Calificacion:
    id: Optional[str]
    alumno_id: str
    materia_id: str
    nota: float
    fecha: str

    def to_dict(self) -> Dict[str, object]:
        return {
            "id": self.id,
            "alumno_id": self.alumno_id,
            "materia_id": self.materia_id,
            "nota": self.nota,
            "fecha": self.fecha,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, object]) -> "Calificacion":
        return cls(
            id=data.get("id"),  # type: ignore[arg-type]
            alumno_id=data["alumno_id"],  # type: ignore[index]
            materia_id=data["materia_id"],  # type: ignore[index]
            nota=float(data.get("nota", 0.0)),
            fecha=data["fecha"],  # type: ignore[index]
        )
