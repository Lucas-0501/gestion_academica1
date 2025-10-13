"""Modelo de dominio para el plan académico."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class Plan:
    id: Optional[str]
    nombre: str
    descripcion: str
    materias: List[str] = field(default_factory=list)

    def addList(self, materia_ids: List[str]) -> None:
        for materia_id in materia_ids:
            if materia_id not in self.materias:
                self.materias.append(materia_id)

    def to_dict(self) -> Dict[str, object]:
        return {
            "id": self.id,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "materias": list(self.materias),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, object]) -> "Plan":
        return cls(
            id=data.get("id"),  # type: ignore[arg-type]
            nombre=data["nombre"],  # type: ignore[index]
            descripcion=data.get("descripcion", ""),  # type: ignore[arg-type]
            materias=list(data.get("materias", [])),  # type: ignore[arg-type]
        )
