from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_user_success(mock_db_session):
    user_data = {"username": "testuser", "email": "test@example.com", "password": "password"}
    response = client.post("/api/user/", json=user_data)
    assert response.status_code == 201
    assert response.json()["username"] == "testuser"
    assert response.json()["email"] == "test@example.com"


def test_create_user_failure_due_to_invalid_email(mock_db_session):
    user_data = {"username": "newuser", "email": "notanemail", "password": "password"}
    response = client.post("/api/user/", json=user_data)
    assert response.status_code == 400
    assert response.json()["detail"] is not None
    assert "Incorrect request body" in response.json()["detail"]


def test_create_user_failure_due_to_missing_password(mock_db_session):
    user_data = {"username": "newuser", "email": "test@example.com"}
    response = client.post("/api/user/", json=user_data)
    assert response.status_code == 400
    assert "Incorrect request body" in response.json()["detail"]
