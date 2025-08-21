import pytest
from fastapi.testclient import TestClient
from src.main import app


@pytest.fixture
def client():
    return TestClient(app)


def test_create_task(client):
    response = client.post("/tasks", json={
        "title": "Test Task",
        "description": "Test Description"
    })

    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")

    assert response.status_code == 201
    assert response.json()["title"] == "Test Task"


def test_get_tasks_list(client):
    response = client.get("/tasks")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
