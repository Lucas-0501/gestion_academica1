"""Compatibilidad: reexporta la clase Docente desde app.models.USRs."""

from app.models.USRs.docente import Docente

__all__ = ["Docente"]
