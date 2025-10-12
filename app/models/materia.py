"""Materia domain model."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class Materia:
    id: Optional[str]
    nombre: str
    codigo: str
    descripcion: str

    def to_dict(self) -> Dict[str, object]:
        return {
            "id": self.id,
            "nombre": self.nombre,
            "codigo": self.codigo,
            "descripcion": self.descripcion,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, object]) -> "Materia":
        return cls(
            id=data.get("id"),  # type: ignore[arg-type]
            nombre=data["nombre"],  # type: ignore[index]
            codigo=data["codigo"],  # type: ignore[index]
            descripcion=data.get("descripcion", ""),  # type: ignore[arg-type]
        )
