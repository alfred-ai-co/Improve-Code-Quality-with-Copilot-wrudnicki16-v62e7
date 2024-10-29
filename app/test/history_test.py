import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.api.dependencies.sqldb import get_db
from app.db_models.base import Base
from app.api_models.history import HistoryCreate, HistoryUpdate

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(scope="module")
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_create_history(test_db):
    response = client.post("/api/history/", json={"entity_type": "project", "entity_id": 1, "change_type": "create","user_id": 1, "details": "Project created"})
    assert response.status_code == 200
    assert response.json()["entity_type"] == "project"
    assert response.json()["entity_id"] == 1

    response = client.post("/api/history/", json={"entity_type": "ticket", "entity_id": 1, "change_type": "create", "user_id": 1, "details": "Ticket created"})
    assert response.status_code == 200
    assert response.json()["entity_type"] == "ticket"
    assert response.json()["entity_id"] == 1

def test_get_history_by_entity_id(test_db):
    response = client.post("/api/history", json={"entity_type": "project", "entity_id": 2, "change_type": "create", "user_id": 1, "details": "Project created"})
    response = client.post("/api/history", json={"entity_type": "ticket", "entity_id": 2, "change_type": "create", "user_id": 1, "details": "Ticket created"})

    response = client.get("/api/history/2?entity_type=project&offset=0&limit=20")
    assert response.status_code == 200
    assert len(response.json()) > 0
    assert response.json()[0]["entity_type"] == "project"
    assert response.json()[0]["entity_id"] == 2

    response = client.get("/api/history/2?entity_type=ticket&offset=0&limit=20")
    assert response.status_code == 200
    assert len(response.json()) > 0
    assert response.json()[0]["entity_type"] == "ticket"
    assert response.json()[0]["entity_id"] == 2

def test_update_history(test_db):
    response = client.post("/api/history", json={"entity_type": "project", "entity_id": 3, "change_type": "create", "user_id": 1, "details": "Project created"})
    history_id = response.json()["id"]

    update_data = {"entity_type": "project", "entity_id": 3, "change_type": "update", "user_id": 1, "details": "Project updated"}
    response = client.put(f"/api/history/{history_id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["change_type"] == "update"
    assert response.json()["details"] == "Project updated"

def test_delete_history(test_db):
    response = client.post("/api/history", json={"entity_type": "project", "entity_id": 4, "change_type": "create", "user_id": 1, "details": "Project created"})
    history_id = response.json()["id"]

    response = client.delete(f"/api/history/{history_id}")
    assert response.status_code == 200
    assert response.json()["id"] == history_id

    response = client.get(f"/api/history/4?entity_type=project&offset=0&limit=20")
    assert response.status_code == 200
    assert len(response.json()) == 0

# Additional tests for invalid or missing data
def test_create_history_missing_entity_id(test_db):
    response = client.post("/api/history/", json={"entity_type": "project", "change_type": "create", "user_id": 1, "details": "Project created"})
    assert response.status_code == 422  # Unprocessable Entity

def test_create_history_invalid_entity_type(test_db):
    response = client.post("/api/history/", json={"entity_type": "invalid_type", "entity_id": 1, "change_type": "create", "user_id": 1, "details": "Invalid entity type"})
    assert response.status_code == 422  # Unprocessable Entity

def test_update_history_invalid_change_type(test_db):
    response = client.post("/api/history", json={"entity_type": "project", "entity_id": 5, "change_type": "create", "user_id": 1, "details": "Project created"})
    history_id = response.json()["id"]

    update_data = {"entity_type": "project", "entity_id": 5, "change_type": "invalid_change", "user_id": 1}
    response = client.put(f"/api/history/{history_id}", json=update_data)
    assert response.status_code == 422  # Unprocessable Entity

def test_update_history_missing_change_type(test_db):
    response = client.post("/api/history", json={"entity_type": "project", "entity_id": 6, "change_type": "create", "user_id": 1, "details": "Project created"})
    history_id = response.json()["id"]

    update_data = {"entity_type": "project", "entity_id": 6, "user_id": 1, "details": "Missing change_type"}
    response = client.put(f"/api/history/{history_id}", json=update_data)
    assert response.status_code == 422  # Unprocessable Entity

def test_delete_history_nonexistent_id(test_db):
    response = client.delete("/api/history/9999")
    assert response.status_code == 404  # Not Found

# Integration tests for history interactions with projects and tickets
def test_ticket_status_update_creates_history(test_db):
    # Create a ticket
    response = client.post("/api/tickets", json={"title": "Test Ticket", "status": "open", "project_id": 1, "description": "Test description", "priority": "low", "kanban_status_id": 1})
    ticket_id = response.json()["id"]

    # Update ticket status
    update_data = {"title": "Test Ticket", "status": "closed", "project_id": 1, "description": "Test description", "priority": "low", "kanban_status_id": 1}
    response = client.put(f"/api/tickets/{ticket_id}", json=update_data)
    assert response.status_code == 200

    # Check history record
    response = client.get(f"/api/history/{ticket_id}?entity_type=ticket&offset=0&limit=20")
    assert response.status_code == 200
    assert len(response.json()) > 0
    assert response.json()[0]["change_type"] == "update"
    assert response.json()[0]["details"] == "Status changed to closed"

def test_foreign_key_constraints(test_db):
    # Create a history record with a non-existent project ID
    response = client.post("/api/history/", json={"entity_type": "project", "entity_id": 9999, "change_type": "create", "user_id": 1, "details": "Invalid project"})
    assert response.status_code == 422  # Unprocessable Entity

    # Create a history record with a non-existent ticket ID
    response = client.post("/api/history/", json={"entity_type": "ticket", "entity_id": 9999, "change_type": "create", "user_id": 1, "details": "Invalid ticket"})
    assert response.status_code == 422  # Unprocessable Entity
