"""Alumno domain model."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional

from .usuario import Usuario


@dataclass
class Alumno(Usuario):
    materiasInscripto: List[str] = field(default_factory=list)
    examenesInscripto: List[str] = field(default_factory=list)
    plan_id: Optional[str] = None
    cohorte_id: Optional[str] = None

    def inscribirseMateria(self, materia_id: str) -> None:
        if materia_id not in self.materiasInscripto:
            self.materiasInscripto.append(materia_id)

    def inscribirseExamen(self, examen_id: str) -> None:
        if examen_id not in self.examenesInscripto:
            self.examenesInscripto.append(examen_id)

    def to_dict(self) -> Dict[str, object]:
        data = super().to_dict()
        data.update(
            {
                "materiasInscripto": list(self.materiasInscripto),
                "examenesInscripto": list(self.examenesInscripto),
                "plan_id": self.plan_id,
                "cohorte_id": self.cohorte_id,
            }
        )
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, object]) -> "Alumno":
        return cls(
            id=data.get("id"),  # type: ignore[arg-type]
            nombre=data["nombre"],  # type: ignore[index]
            email=data["email"],  # type: ignore[index]
            password=data["password"],  # type: ignore[index]
            rol=data.get("rol", "alumno"),  # type: ignore[arg-type]
            sesion_activa=data.get("sesion_activa", False),  # type: ignore[arg-type]
            materiasInscripto=list(data.get("materiasInscripto", [])),  # type: ignore[arg-type]
            examenesInscripto=list(data.get("examenesInscripto", [])),  # type: ignore[arg-type]
            plan_id=data.get("plan_id"),  # type: ignore[arg-type]
            cohorte_id=data.get("cohorte_id"),  # type: ignore[arg-type]
        )
