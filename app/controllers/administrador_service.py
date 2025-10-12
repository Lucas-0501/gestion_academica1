"""Service layer for administrator use cases."""

from __future__ import annotations

from typing import List, Optional

from app.models.administrador import Administrador
from app.models.alumno import Alumno
from app.models.cohorte import Cohorte
from app.models.curso import Curso
from app.models.dbbroker import DBBroker
from app.models.docente import Docente
from app.models.materia import Materia
from app.models.plan import Plan


class AdministradorService:
    def __init__(self, broker: Optional[DBBroker] = None) -> None:
        self.broker = broker or DBBroker()

    def crearMateria(self, admin: Administrador, nombre: str, codigo: str, descripcion: str) -> Materia:
        materia = admin.crearMateria(nombre, codigo, descripcion)
        self.broker.guardarObjeto(materia)
        return materia

    def registrarAlumno(self, nombre: str, email: str, password: str) -> Alumno:
        alumno = Alumno(
            id=None,
            nombre=nombre,
            email=email,
            password=password,
            rol="alumno",
        )
        self.broker.guardarObjeto(alumno)
        return alumno

    def registrarDocente(self, nombre: str, email: str, password: str) -> Docente:
        docente = Docente(
            id=None,
            nombre=nombre,
            email=email,
            password=password,
            rol="docente",
        )
        self.broker.guardarObjeto(docente)
        return docente

    def crearPlan(self, admin: Administrador, nombre: str, descripcion: str) -> Plan:
        plan = admin.crearPlan(nombre, descripcion)
        self.broker.guardarObjeto(plan)
        return plan

    def asignarMateriasAPlan(self, plan_id: str, materias_ids: List[str]) -> Plan:
        data = self.broker.obtenerPorId("Plan", plan_id)
        if not data:
            raise ValueError("Plan no encontrado")
        plan = Plan.from_dict(data)
        plan.addList(materias_ids)
        self.broker.actualizarObjeto(plan)
        return plan

    def crearCohorte(
        self,
        admin: Administrador,
        nombre: str,
        plan_id: str,
        alumnos_ids: Optional[List[str]] = None,
    ) -> Cohorte:
        cohorte = admin.crearCohorte(nombre, plan_id, alumnos_ids)
        self.broker.guardarObjeto(cohorte)
        if alumnos_ids:
            self._asignar_plan_y_cohorte_a_alumnos(alumnos_ids, plan_id, cohorte.id)  # type: ignore[arg-type]
        return cohorte

    def _asignar_plan_y_cohorte_a_alumnos(
        self, alumnos_ids: List[str], plan_id: str, cohorte_id: Optional[str]
    ) -> None:
        for alumno_id in alumnos_ids:
            data = self.broker.obtenerPorId("Usuario", alumno_id)
            if not data or data.get("rol") != "alumno":
                continue
            alumno = Alumno.from_dict(data)
            alumno.plan_id = plan_id
            alumno.cohorte_id = cohorte_id
            self.broker.actualizarObjeto(alumno)

    def crearCurso(
        self,
        admin: Administrador,
        nombre: str,
        materia_id: str,
        cohorte_id: Optional[str],
        docente_id: Optional[str],
    ) -> Curso:
        curso = admin.crearCurso(nombre, materia_id, cohorte_id, docente_id)
        self.broker.guardarObjeto(curso)
        return curso

    def asignarDocente(self, curso_id: str, docente_id: str) -> Curso:
        data = self.broker.obtenerPorId("Curso", curso_id)
        if not data:
            raise ValueError("Curso no encontrado")
        curso = Curso.from_dict(data)
        curso.asignarDocente(docente_id)
        self.broker.actualizarObjeto(curso)
        return curso

    def listarMaterias(self) -> List[Materia]:
        return [Materia.from_dict(item) for item in self.broker.listar("Materia")]

    def listarPlanes(self) -> List[Plan]:
        return [Plan.from_dict(item) for item in self.broker.listar("Plan")]

    def listarCohortes(self) -> List[Cohorte]:
        return [Cohorte.from_dict(item) for item in self.broker.listar("Cohorte")]

    def listarDocentes(self) -> List[Docente]:
        usuarios = self.broker.listar("Usuario")
        docentes = [
            item for item in usuarios if item.get("rol") == "docente"
        ]
        return [Docente.from_dict(item) for item in docentes]  # type: ignore[arg-type]

    def listarAlumnos(self) -> List[Alumno]:
        usuarios = self.broker.listar("Usuario")
        alumnos = [
            item for item in usuarios if item.get("rol") == "alumno"
        ]
        return [Alumno.from_dict(item) for item in alumnos]  # type: ignore[arg-type]
