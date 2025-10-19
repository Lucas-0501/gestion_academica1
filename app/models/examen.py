"""Modelo de dominio para examen."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class Examen:
    id: Optional[str]
    nombre: str
    materia_id: str
    fecha: str
    curso_id: Optional[str] = None
    correlativas: List[str] = field(default_factory=list)
    cupo: Optional[int] = None

    def to_dict(self) -> Dict[str, object]:
        return {
            "id": self.id,
            "nombre": self.nombre,
            "materia_id": self.materia_id,
            "fecha": self.fecha,
            "curso_id": self.curso_id,
            "correlativas": list(self.correlativas),
            "cupo": self.cupo,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, object]) -> "Examen":
        return cls(
            id=data.get("id"),  # type: ignore[arg-type]
            nombre=data.get("nombre", "Examen"),  # type: ignore[arg-type]
            materia_id=data["materia_id"],  # type: ignore[index]
            fecha=data["fecha"],  # type: ignore[index]
            curso_id=data.get("curso_id"),  # type: ignore[arg-type]
            correlativas=list(data.get("correlativas", [])),  # type: ignore[arg-type]
            cupo=data.get("cupo"),  # type: ignore[arg-type]
        )
