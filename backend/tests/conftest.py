import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app import criar_app


@pytest.fixture
def cliente(tmp_path):
    app = criar_app(tmp_path / "teste.db")
    app.config["TESTING"] = True
    return app.test_client()
