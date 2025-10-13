"""Compatibilidad: reexporta la clase Alumno desde app.models.USRs."""

from app.models.USRs.alumno import Alumno

__all__ = ["Alumno"]
