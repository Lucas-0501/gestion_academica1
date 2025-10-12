"""In-memory broker that simulates database persistence."""

from __future__ import annotations

import threading
import uuid
from typing import Any, Dict, List, Optional, Type, TypeVar

from app.utils.mapper import Mapper

T = TypeVar("T")


class DBBroker:
    """Singleton that manages storage for domain entities."""

    _instance: Optional["DBBroker"] = None
    _lock = threading.Lock()

    def __new__(cls) -> "DBBroker":
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialize()
        return cls._instance

    _ALIAS = {
        "Administrador": "Usuario",
        "Alumno": "Usuario",
        "Docente": "Usuario",
    }

    def _initialize(self) -> None:
        self._store: Dict[str, List[Dict[str, Any]]] = {}
        for collection in {
            "Usuario",
            "Materia",
            "Plan",
            "Cohorte",
            "Curso",
            "Examen",
            "Asistencia",
            "Calificacion",
        }:
            self._store[collection] = Mapper.load(collection)

    def _resolve_collection(self, name: str) -> str:
        return self._ALIAS.get(name, name)

    def _persist(self, collection: str) -> None:
        canonical = self._resolve_collection(collection)
        Mapper.save(canonical, self._store.get(canonical, []))

    def _ensure_id(self, obj: Any) -> str:
        if not getattr(obj, "id", None):
            setattr(obj, "id", str(uuid.uuid4()))
        return obj.id

    def guardarObjeto(self, obj: Any) -> Dict[str, Any]:
        """Persist a new domain object."""
        collection = self._resolve_collection(obj.__class__.__name__)
        self._ensure_id(obj)
        data = obj.to_dict()
        existing = self._store.setdefault(collection, [])
        if any(item["id"] == data["id"] for item in existing):
            raise ValueError(f"{collection} with id {data['id']} already exists")
        existing.append(data)
        self._persist(collection)
        return data

    def obtener(self, clase: Type[T], obj_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve raw data for the given class and id."""
        collection = (
            clase.__name__ if not isinstance(clase, str) else clase
        )
        return self.obtenerPorId(collection, obj_id)

    def obtenerPorId(self, clase: str, obj_id: str) -> Optional[Dict[str, Any]]:
        canonical = self._resolve_collection(clase)
        for item in self._store.get(canonical, []):
            if item.get("id") == obj_id:
                return item
        return None

    def listar(self, clase: str) -> List[Dict[str, Any]]:
        canonical = self._resolve_collection(clase)
        return list(self._store.get(canonical, []))

    def actualizarObjeto(self, obj: Any) -> Dict[str, Any]:
        if isinstance(obj, dict):
            data = obj
            collection = data.get("class") or data.get("_collection")
            if not collection:
                raise ValueError("Collection identifier missing in dict payload")
        else:
            collection = obj.__class__.__name__
            data = obj.to_dict()
        canonical = self._resolve_collection(collection)
        existing = self._store.setdefault(canonical, [])
        for index, item in enumerate(existing):
            if item["id"] == data["id"]:
                existing[index] = data
                self._persist(canonical)
                return data
        raise ValueError(
            f"{canonical} with id {data['id']} not found for update"
        )

    def eliminarObjeto(self, clase: str, obj_id: str) -> None:
        collection = (
            clase if isinstance(clase, str) else clase.__name__
        )
        canonical = self._resolve_collection(collection)
        items = self._store.get(canonical, [])
        filtered = [item for item in items if item.get("id") != obj_id]
        self._store[canonical] = filtered
        self._persist(canonical)

    def addList(
        self, clase: str, obj_id: str, field: str, values: List[Any]
    ) -> Dict[str, Any]:
        """Append values into a list attribute and persist the parent object."""
        canonical = self._resolve_collection(clase)
        record = self.obtenerPorId(canonical, obj_id)
        if record is None:
            raise ValueError(f"{canonical} with id {obj_id} not found")
        current = record.setdefault(field, [])
        for value in values:
            if value not in current:
                current.append(value)
        self._persist(canonical)
        return record

    def reset_store(self) -> None:
        """Utility for tests to clear the in-memory store."""
        for collection in self._store:
            self._store[collection] = []
            self._persist(collection)
