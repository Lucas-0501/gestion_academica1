"""Utilidades para persistir objetos de dominio en archivos JSON."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List


class Mapper:
    """Mapper básico que guarda colecciones como listas JSON."""

    _DATA_DIR = Path(__file__).resolve().parents[2] / "data"
    _FILE_MAP = {
        "Usuario": "usuarios.json",
        "Administrador": "usuarios.json",
        "Alumno": "usuarios.json",
        "Docente": "usuarios.json",
        "Materia": "materias.json",
        "Plan": "planes.json",
        "Cohorte": "cohortes.json",
        "Curso": "cursos.json",
        "Examen": "examenes.json",
        "Asistencia": "asistencias.json",
        "Calificacion": "calificaciones.json",
    }

    @classmethod
    def _get_path(cls, collection: str) -> Path:
        filename = cls._FILE_MAP.get(collection, f"{collection.lower()}s.json")
        path = cls._DATA_DIR / filename
        path.parent.mkdir(parents=True, exist_ok=True)
        if not path.exists():
            path.write_text("[]", encoding="utf-8")
        return path

    @classmethod
    def load(cls, collection: str) -> List[Dict[str, Any]]:
        path = cls._get_path(collection)
        try:
            with path.open("r", encoding="utf-8") as file:
                return json.load(file)
        except json.JSONDecodeError:
            return []

    @classmethod
    def save(cls, collection: str, data: List[Dict[str, Any]]) -> None:
        path = cls._get_path(collection)
        with path.open("w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
