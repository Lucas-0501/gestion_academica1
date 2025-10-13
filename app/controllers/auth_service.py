"""Servicio de aplicación para los flujos de autenticación."""

from __future__ import annotations

from typing import Dict, Optional

from app.models.USRs import Administrador, Alumno, Docente, Usuario
from app.models.dbbroker import DBBroker


class AuthService:
    def __init__(self, broker: Optional[DBBroker] = None) -> None:
        self.broker = broker or DBBroker()

    def iniciarSesion(self, email: str, password: str, rol: Optional[str] = None) -> Usuario:
        usuarios = self.broker.listar("Usuario")
        for data in usuarios:
            if data["email"] == email and data["password"] == password:
                if rol and data.get("rol") != rol:
                    continue
                return self._build_usuario(data)
        raise ValueError("Credenciales invalidas")

    def _build_usuario(self, data: Dict[str, object]) -> Usuario:
        tipo = data.get("type") or data.get("rol", "").capitalize()
        if tipo == "Administrador":
            return Administrador.from_dict(data)
        if tipo == "Alumno":
            return Alumno.from_dict(data)
        if tipo == "Docente":
            return Docente.from_dict(data)
        return Usuario.from_dict(data)

    def obtener_usuario(self, usuario_id: str) -> Optional[Usuario]:
        data = self.broker.obtenerPorId("Usuario", usuario_id)
        return self._build_usuario(data) if data else None
