import pytest
from fastapi.testclient import TestClient

from src.main import app


@pytest.fixture
def client() -> TestClient:
    """Create test client."""
    return TestClient(app)


def test_create_task(client: TestClient) -> None:
    """Test task creation via API."""
    response = client.post(
        "/tasks/", json={"title": "Test Task", "description": "Test Description"}
    )

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Task"


def test_get_tasks_list(client: TestClient) -> None:
    """Test getting tasks list via API."""
    response = client.get("/tasks/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
