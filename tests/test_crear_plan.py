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


def test_crear_plan_valido(admin_client):
    resp = admin_client.post(
        "/admin/crear_plan",
        data={"nombre": "Ingeniería en Sistemas", "descripcion": "Plan base"},
        follow_redirects=False,
    )
    query = _extract_query(resp)
    assert resp.status_code == 303
    assert query.get("success") == ["Plan académico creado con éxito"]


def test_crear_plan_nombre_vacio(admin_client):
    resp = admin_client.post(
        "/admin/crear_plan",
        data={"nombre": "", "descripcion": ""},
        follow_redirects=False,
    )
    query = _extract_query(resp)
    assert resp.status_code == 303
    assert query.get("error") == ["Debe ingresar nombre"]


def test_crear_plan_nombre_espacios(admin_client):
    resp = admin_client.post(
        "/admin/crear_plan",
        data={"nombre": "   ", "descripcion": ""},
        follow_redirects=False,
    )
    query = _extract_query(resp)
    assert resp.status_code == 303
    assert query.get("error") == ["Debe ingresar nombre"]


def test_crear_plan_nombre_con_especiales(admin_client):
    resp = admin_client.post(
        "/admin/crear_plan",
        data={"nombre": "Ingeniería@Sistemas", "descripcion": ""},
        follow_redirects=False,
    )
    query = _extract_query(resp)
    assert resp.status_code == 303
    assert query.get("error") == ["El nombre no admite caracteres especiales"]


def test_crear_plan_nombre_no_excede_limite(admin_client):
    resp = admin_client.post(
        "/admin/crear_plan",
        data={"nombre": "ABCD2025", "descripcion": ""},
        follow_redirects=False,
    )
    query = _extract_query(resp)
    assert resp.status_code == 303
    assert query.get("success") == ["Plan académico creado con éxito"]


def test_crear_plan_nombre_excede_limite(admin_client):
    resp = admin_client.post(
        "/admin/crear_plan",
        data={"nombre": "A" * 51, "descripcion": ""},
        follow_redirects=False,
    )
    query = _extract_query(resp)
    assert resp.status_code == 303
    assert query.get("error") == ["Nombre máximo 50 caracteres"]


def test_crear_plan_nombre_duplicado(admin_client):
    primera = admin_client.post(
        "/admin/crear_plan",
        data={"nombre": "Ingeniería en Sistemas", "descripcion": ""},
        follow_redirects=False,
    )
    assert primera.status_code == 303
    segunda = admin_client.post(
        "/admin/crear_plan",
        data={"nombre": "Ingeniería en Sistemas", "descripcion": "Otro"},
        follow_redirects=False,
    )
    query = _extract_query(segunda)
    assert segunda.status_code == 303
    assert query.get("error") == ["Plan ya registrado"]
