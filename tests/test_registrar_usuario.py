from urllib.parse import parse_qs, urlparse

import pytest
from fastapi.testclient import TestClient

from app.main import create_app
from app.models.dbbroker import DBBroker


def _extract_query(resp):
    location = resp.headers.get("location", "")
    return parse_qs(urlparse(location).query)


@pytest.fixture
def admin_client(mapper_tmp_dir):
    app = create_app()
    with TestClient(app) as client:
        login = client.post(
            "/auth/login",
            data={"usuario": "admin@demo.com", "password": "1234"},
            follow_redirects=False,
        )
        assert login.status_code == 303
        yield client
    DBBroker._instance = None


def test_registro_usuario_valido(admin_client):
    resp = admin_client.post(
        "/admin/registrar_usuario",
        data={"nombre": "Juan Perez", "email": "juan@mail.com", "password": "1234", "tipo": "alumno"},
        follow_redirects=False,
    )
    query = _extract_query(resp)
    assert resp.status_code == 303
    assert query.get("success") == ["Usuario creado exitosamente"]
    usuarios = DBBroker().listar("Usuario")
    assert any(u["email"] == "juan@mail.com" and u.get("rol") == "alumno" for u in usuarios)


def test_registro_usuario_nombre_vacio(admin_client):
    resp = admin_client.post(
        "/admin/registrar_usuario",
        data={"nombre": " ", "email": "juan@mail.com", "password": "1234", "tipo": "alumno"},
        follow_redirects=False,
    )
    query = _extract_query(resp)
    assert resp.status_code == 303
    assert query.get("error") == ["El campo nombre es obligatorio"]


def test_registro_usuario_nombre_con_numeros(admin_client):
    resp = admin_client.post(
        "/admin/registrar_usuario",
        data={"nombre": "Juan123", "email": "juan@mail.com", "password": "1234", "tipo": "alumno"},
        follow_redirects=False,
    )
    query = _extract_query(resp)
    assert resp.status_code == 303
    assert query.get("error") == ["El nombre solo puede contener letras y espacios"]


def test_registro_usuario_correo_invalido(admin_client):
    resp = admin_client.post(
        "/admin/registrar_usuario",
        data={"nombre": "Juan Perez", "email": "juanmail.com", "password": "1234", "tipo": "alumno"},
        follow_redirects=False,
    )
    query = _extract_query(resp)
    assert resp.status_code == 303
    assert query.get("error") == ["Formato de correo incorrecto"]


def test_registro_usuario_correo_duplicado(admin_client):
    primera = admin_client.post(
        "/admin/registrar_usuario",
        data={"nombre": "Juan Perez", "email": "existente@mail.com", "password": "1234", "tipo": "alumno"},
        follow_redirects=False,
    )
    assert primera.status_code == 303
    segunda = admin_client.post(
        "/admin/registrar_usuario",
        data={"nombre": "Juan Perez", "email": "existente@mail.com", "password": "1234", "tipo": "alumno"},
        follow_redirects=False,
    )
    query = _extract_query(segunda)
    assert segunda.status_code == 303
    assert query.get("error") == ["El correo ya está registrado"]


def test_registro_usuario_nombre_muy_largo(admin_client):
    resp = admin_client.post(
        "/admin/registrar_usuario",
        data={
            "nombre": "Nombre muy largo con más de cincuenta caracteres totales",
            "email": "juan@mail.com",
            "password": "1234",
            "tipo": "docente",
        },
        follow_redirects=False,
    )
    query = _extract_query(resp)
    assert resp.status_code == 303
    assert query.get("error") == ["Nombre máximo 50 caracteres"]
