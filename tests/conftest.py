from pathlib import Path
import sys

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.models.dbbroker import DBBroker
from app.utils.mapper import Mapper


@pytest.fixture
def mapper_tmp_dir(tmp_path, monkeypatch):
    """Redirects Mapper storage to an isolated temp directory for tests."""
    data_dir = tmp_path / "data"
    monkeypatch.setattr(Mapper, "_DATA_DIR", data_dir, raising=False)
    DBBroker._instance = None
    yield data_dir
    DBBroker._instance = None


@pytest.fixture
def isolated_broker(mapper_tmp_dir):
    """Provides a fresh DBBroker instance backed by the isolated storage."""
    broker = DBBroker()
    yield broker
    DBBroker._instance = None
