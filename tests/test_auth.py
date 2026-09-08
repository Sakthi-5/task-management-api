from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_create_user():
    response = client.post(
        "/users",
        json={
            "name": "Test User",
            "email": "testuser@gmail.com",
            "password": "Test@123"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "password" not in data
    assert data["email"] == "testuser@gmail.com"


def test_login_success():
    response = client.post(
        "/login",
        json={
            "email": "testuser@gmail.com",
            "password": "Test@123"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password():
    response = client.post(
        "/login",
        json={
            "email": "testuser@gmail.com",
            "password": "WrongPassword"
        }
    )

    assert response.status_code == 401


def test_login_non_existing_user():
    response = client.post(
        "/login",
        json={
            "email": "doesnotexist@gmail.com",
            "password": "Test@123"
        }
    )

    assert response.status_code == 401