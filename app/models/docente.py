"""Docente domain model."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List

from .usuario import Usuario


@dataclass
class Docente(Usuario):
    materiasAsignadas: List[str] = field(default_factory=list)

    def asignarMateria(self, materia_id: str) -> None:
        if materia_id not in self.materiasAsignadas:
            self.materiasAsignadas.append(materia_id)

    def cargarCalificacion(self, alumno_id: str, materia_id: str, nota: float) -> Dict[str, object]:
        return {
            "alumno_id": alumno_id,
            "materia_id": materia_id,
            "nota": nota,
        }

    def to_dict(self) -> Dict[str, object]:
        data = super().to_dict()
        data.update(
            {
                "materiasAsignadas": list(self.materiasAsignadas),
            }
        )
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, object]) -> "Docente":
        return cls(
            id=data.get("id"),  # type: ignore[arg-type]
            nombre=data["nombre"],  # type: ignore[index]
            email=data["email"],  # type: ignore[index]
            password=data["password"],  # type: ignore[index]
            rol=data.get("rol", "docente"),  # type: ignore[arg-type]
            sesion_activa=data.get("sesion_activa", False),  # type: ignore[arg-type]
            materiasAsignadas=list(data.get("materiasAsignadas", [])),  # type: ignore[arg-type]
        )
