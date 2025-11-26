import pytest
from fastapi.testclient import TestClient

from app.main import create_app
from app.models.dbbroker import DBBroker


@pytest.fixture
def client(mapper_tmp_dir):
    app = create_app()
    with TestClient(app) as client:
        yield client
    DBBroker._instance = None


def test_admin_route_sin_login_muestra_pagina(client):
    resp = client.get("/admin/crear_plan")
    assert resp.status_code == 401
    assert "Acceso restringido" in resp.text
    assert "Volver al inicio de sesión" in resp.text


def test_admin_route_sin_permisos_muestra_pagina(client):
    login = client.post(
        "/auth/login",
        data={"usuario": "alumno1@demo.com", "password": "1234"},
        follow_redirects=False,
    )
    assert login.status_code == 303
    resp = client.get("/admin/crear_plan")
    assert resp.status_code == 403
    assert "Acceso restringido" in resp.text
