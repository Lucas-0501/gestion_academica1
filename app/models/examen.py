"""Examen domain model."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class Examen:
    id: Optional[str]
    materia_id: str
    fecha: str
    cupo: Optional[int] = None

    def to_dict(self) -> Dict[str, object]:
        return {
            "id": self.id,
            "materia_id": self.materia_id,
            "fecha": self.fecha,
            "cupo": self.cupo,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, object]) -> "Examen":
        return cls(
            id=data.get("id"),  # type: ignore[arg-type]
            materia_id=data["materia_id"],  # type: ignore[index]
            fecha=data["fecha"],  # type: ignore[index]
            cupo=data.get("cupo"),  # type: ignore[arg-type]
        )
