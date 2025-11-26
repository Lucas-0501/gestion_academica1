from urllib.parse import parse_qs, urlparse

import pytest
from fastapi.testclient import TestClient

from app.main import create_app
from app.models.dbbroker import DBBroker


@pytest.fixture
def client(mapper_tmp_dir):
    """Entrega un TestClient con almacenamiento aislado gracias a mapper_tmp_dir."""
    app = create_app()
    with TestClient(app) as client:
        yield client
    DBBroker._instance = None


def _extract_error(resp):
    location = resp.headers.get("location", "")
    query = parse_qs(urlparse(location).query)
    return query.get("error", [None])[0]


def test_login_ok_redirige_dashboard(client):
    resp = client.post(
        "/auth/login",
        data={"usuario": "jperez", "password": "clave123"},
        follow_redirects=False,
    )
    assert resp.status_code == 303
    assert resp.headers["location"].endswith("/dashboard")


def test_campo_usuario_vacio(client):
    resp = client.post(
        "/auth/login",
        data={"usuario": "", "password": "clave123"},
        follow_redirects=False,
    )
    assert resp.status_code == 303
    assert _extract_error(resp) == "El campo usuario es obligatorio"


def test_campo_password_vacio(client):
    resp = client.post(
        "/auth/login",
        data={"usuario": "jperez", "password": ""},
        follow_redirects=False,
    )
    assert resp.status_code == 303
    assert _extract_error(resp) == "El campo contraseña es obligatorio"


def test_credenciales_invalidas(client):
    resp = client.post(
        "/auth/login",
        data={"usuario": "jperez", "password": "incorrecta1"},
        follow_redirects=False,
    )
    assert resp.status_code == 303
    assert _extract_error(resp) == "Credenciales invalidas"


def test_usuario_con_numeros(client):
    resp = client.post(
        "/auth/login",
        data={"usuario": "user123", "password": "clave123"},
        follow_redirects=False,
    )
    assert resp.status_code == 303
    assert resp.headers["location"].endswith("/dashboard")


def test_usuario_muy_corto(client):
    resp = client.post(
        "/auth/login",
        data={"usuario": "ab", "password": "clave123"},
        follow_redirects=False,
    )
    assert resp.status_code == 303
    assert _extract_error(resp) == "Usuario debe tener minimo 3 caracteres"


def test_usuario_muy_largo(client):
    resp = client.post(
        "/auth/login",
        data={"usuario": "uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu", "password": "clave123"},
        follow_redirects=False,
    )
    assert resp.status_code == 303
    assert _extract_error(resp) == "Usuario maximo 40 caracteres"


def test_password_sin_numeros(client):
    resp = client.post(
        "/auth/login",
        data={"usuario": "jperez", "password": "sololetras"},
        follow_redirects=False,
    )
    assert resp.status_code == 303
    assert _extract_error(resp) == "La contraseña debe contener al menos 1 número"


def test_cuenta_bloqueada(client):
    resp = client.post(
        "/auth/login",
        data={"usuario": "user_bloqueado", "password": "clave123"},
        follow_redirects=False,
    )
    assert resp.status_code == 303
    assert _extract_error(resp) == "Cuenta bloqueada. Contacte al administrador"


def test_usuario_con_caracteres_especiales(client):
    resp = client.post(
        "/auth/login",
        data={"usuario": "user@#", "password": "clave123"},
        follow_redirects=False,
    )
    assert resp.status_code == 303
    assert _extract_error(resp) == "Usuario solo puede contener letras y numeros"
