"""Modelo de dominio para cohorte."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class Cohorte:
    id: Optional[str]
    nombre: str
    plan_id: str
    alumnos: List[str] = field(default_factory=list)

    def asignarAlumno(self, alumno_id: str) -> None:
        if alumno_id not in self.alumnos:
            self.alumnos.append(alumno_id)

    def to_dict(self) -> Dict[str, object]:
        return {
            "id": self.id,
            "nombre": self.nombre,
            "plan_id": self.plan_id,
            "alumnos": list(self.alumnos),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, object]) -> "Cohorte":
        return cls(
            id=data.get("id"),  # type: ignore[arg-type]
            nombre=data["nombre"],  # type: ignore[index]
            plan_id=data["plan_id"],  # type: ignore[index]
            alumnos=list(data.get("alumnos", [])),  # type: ignore[arg-type]
        )
