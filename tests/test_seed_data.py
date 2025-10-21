from app.main import seed_data
from app.models.dbbroker import DBBroker


def test_seed_data_popula_datos_base(mapper_tmp_dir):
    seed_data()
    broker = DBBroker()

    usuarios = broker.listar("Usuario")
    emails = {usuario["email"] for usuario in usuarios}
    assert {"admin@demo.com", "alumno1@demo.com", "docente1@demo.com"} <= emails

    materias = broker.listar("Materia")
    assert len(materias) == 2

    planes = broker.listar("Plan")
    assert len(planes) == 1
    assert set(planes[0]["materias"]) == {materia["id"] for materia in materias}

    examenes = broker.listar("Examen")
    assert len(examenes) == 1
    assert examenes[0]["materia_id"] == materias[0]["id"]


def test_seed_data_es_idempotente(mapper_tmp_dir):
    seed_data()
    broker = DBBroker()

    base_state = {
        "usuarios": {usuario["email"] for usuario in broker.listar("Usuario")},
        "materias": {materia["codigo"] for materia in broker.listar("Materia")},
        "planes": len(broker.listar("Plan")),
        "examenes": len(broker.listar("Examen")),
    }

    seed_data()

    assert {usuario["email"] for usuario in broker.listar("Usuario")} == base_state[
        "usuarios"
    ]
    assert {materia["codigo"] for materia in broker.listar("Materia")} == base_state[
        "materias"
    ]
    assert len(broker.listar("Plan")) == base_state["planes"]
    assert len(broker.listar("Examen")) == base_state["examenes"]
