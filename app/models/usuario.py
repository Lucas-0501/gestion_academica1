"""Compatibilidad: reexporta la clase Usuario desde app.models.USRs."""

from app.models.USRs.usuario import Usuario

__all__ = ["Usuario"]
