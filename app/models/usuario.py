"""Domain model definitions for system users."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class Usuario:
    """Base class for all system users."""

    id: Optional[str]
    nombre: str
    email: str
    password: str
    rol: str
    sesion_activa: bool = field(default=False)

    def iniciarSesion(self, password: str) -> bool:
        if self.password == password:
            self.sesion_activa = True
            return True
        return False

    def cerrarSesion(self) -> None:
        self.sesion_activa = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "nombre": self.nombre,
            "email": self.email,
            "password": self.password,
            "rol": self.rol,
            "sesion_activa": self.sesion_activa,
            "type": self.__class__.__name__,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Usuario":
        return cls(
            id=data.get("id"),
            nombre=data["nombre"],
            email=data["email"],
            password=data["password"],
            rol=data["rol"],
            sesion_activa=data.get("sesion_activa", False),
        )
