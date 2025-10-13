"""Modelo de dominio para curso."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class Curso:
    id: Optional[str]
    nombre: str
    materia_id: str
    cohorte_id: Optional[str] = None
    docente_id: Optional[str] = None

    def asignarDocente(self, docente_id: str) -> None:
        self.docente_id = docente_id

    def to_dict(self) -> Dict[str, object]:
        return {
            "id": self.id,
            "nombre": self.nombre,
            "materia_id": self.materia_id,
            "cohorte_id": self.cohorte_id,
            "docente_id": self.docente_id,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, object]) -> "Curso":
        return cls(
            id=data.get("id"),  # type: ignore[arg-type]
            nombre=data["nombre"],  # type: ignore[index]
            materia_id=data["materia_id"],  # type: ignore[index]
            cohorte_id=data.get("cohorte_id"),  # type: ignore[arg-type]
            docente_id=data.get("docente_id"),  # type: ignore[arg-type]
        )
