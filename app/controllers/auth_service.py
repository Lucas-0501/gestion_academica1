"""Servicio de aplicaciÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n para los flujos de autenticaciÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â³n."""

from __future__ import annotations

from typing import Dict, Optional

from app.models.USRs import Administrador, Alumno, Docente, Usuario
from app.models.dbbroker import DBBroker


class AuthService:
    def __init__(self, broker: Optional[DBBroker] = None) -> None:
        self.broker = broker or DBBroker()

    def iniciarSesion(self, usuario: str, password: str, rol: Optional[str] = None) -> Usuario:
        usuarios = self.broker.listar("Usuario")
        for data in usuarios:
            if not self._match_usuario(data, usuario):
                continue
            if data.get("bloqueado"):
                raise ValueError("Cuenta bloqueada. Contacte al administrador")
            if data["password"] == password:
                if rol and data.get("rol") != rol:
                    continue
                return self._build_usuario(data)
            raise ValueError("Credenciales invalidas")
        raise ValueError("Credenciales invalidas")

    def _match_usuario(self, data: Dict[str, object], usuario: str) -> bool:
        return data.get("email") == usuario or data.get("username") == usuario

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