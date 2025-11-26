"""Punto de arranque de la aplicación FastAPI del sistema de gestión académica."""

from __future__ import annotations

from contextlib import asynccontextmanager
from pathlib import Path
from typing import List

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

from app.models.USRs import Administrador, Alumno, Docente
from app.models.dbbroker import DBBroker
from app.models.examen import Examen
from app.models.materia import Materia
from app.models.plan import Plan
from app.router import admin_router, alumno_router, auth_router, docente_router


def create_app() -> FastAPI:
    base_dir = Path(__file__).resolve().parent
    static_dir = base_dir / "static"
    templates = Jinja2Templates(directory=str(base_dir / "templates"))

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        seed_data()
        yield

    app = FastAPI(title="Sistema de Gestion Academica", lifespan=lifespan)
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

    app.include_router(auth_router.router)
    app.include_router(admin_router.router)
    app.include_router(alumno_router.router)
    app.include_router(docente_router.router)

    app.add_middleware(SessionMiddleware, secret_key="super-secret-key")
    app.state.templates = templates

    return app


def seed_data() -> None:
    broker = DBBroker()
    _seed_users(broker)
    _seed_materias_planes(broker)
    _seed_examenes(broker)


def _seed_users(broker: DBBroker) -> None:
    usuarios = broker.listar("Usuario")
    emails = {usuario["email"] for usuario in usuarios}
    if "admin@demo.com" not in emails:
        admin = Administrador(
            id=None,
            nombre="Administrador General",
            email="admin@demo.com",
            password="1234",
            rol="administrador",
        )
        broker.guardarObjeto(admin)
    if "alumno1@demo.com" not in emails:
        alumno = Alumno(
            id=None,
            nombre="Alumno Demo",
            email="alumno1@demo.com",
            password="1234",
            rol="alumno",
        )
        broker.guardarObjeto(alumno)
    if "docente1@demo.com" not in emails:
        docente = Docente(
            id=None,
            nombre="Docente Demo",
            email="docente1@demo.com",
            password="1234",
            rol="docente",
        )
        broker.guardarObjeto(docente)
    if "jperez" not in emails:
        broker.guardarObjeto(
            Alumno(
                id=None,
                nombre="Juan Perez",
                email="jperez",
                password="clave123",
                rol="alumno",
            )
        )
    if "user123" not in emails:
        broker.guardarObjeto(
            Alumno(
                id=None,
                nombre="Usuario Numerico",
                email="user123",
                password="clave123",
                rol="alumno",
            )
        )
    if "user_bloqueado" not in emails:
        broker.guardarObjeto(
            Alumno(
                id=None,
                nombre="Usuario Bloqueado",
                email="user_bloqueado",
                password="clave123",
                rol="alumno",
                bloqueado=True,
            )
        )


def _seed_materias_planes(broker: DBBroker) -> None:
    materias = broker.listar("Materia")
    if not materias:
        algoritmos = Materia(
            id=None,
            nombre="Algoritmos",
            codigo="ALG101",
            descripcion="Introduccion a la Programacion",
        )
        bases = Materia(
            id=None,
            nombre="Bases de Datos",
            codigo="BD201",
            descripcion="Fundamentos de Bases de Datos",
        )
        materias_ids: List[str] = []
        for materia in [algoritmos, bases]:
            data = broker.guardarObjeto(materia)
            materias_ids.append(data["id"])
        plan = Plan(
            id=None,
            nombre="Plan Ingenieria de Software",
            descripcion="Plan base de materias iniciales",
            materias=materias_ids,
        )
        broker.guardarObjeto(plan)


def _seed_examenes(broker: DBBroker) -> None:
    examenes = broker.listar("Examen")
    if not examenes:
        materias = broker.listar("Materia")
        if materias:
            primer_materia = materias[0]
            examen = Examen(
                id=None,
                nombre="Examen Inicial",
                materia_id=primer_materia["id"],
                fecha="2024-07-01",
                curso_id=None,
                correlativas=[],
            )
            broker.guardarObjeto(examen)


app = create_app()
