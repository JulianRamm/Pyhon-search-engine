from app import create_app
import pytest

@pytest.fixture
def app(monkeypatch):
    app = create_app()
    return app