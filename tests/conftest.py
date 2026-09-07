import pytest
from fastapi.testclient import TestClient

from dependencies import get_store
from main import app
from store import Store


@pytest.fixture
def store():
    return Store()


@pytest.fixture
def client(store):
    app.dependency_overrides[get_store] = lambda: store
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
