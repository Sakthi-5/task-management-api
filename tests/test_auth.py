from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def create_test_user(name, email, password):
    response = client.post(
        "/users",
        json={
            "name": name,
            "email": email,
            "password": password
        }
    )

    return response


def test_login_success():

    create_test_user(
        "Test User",
        "testuser@gmail.com",
        "Test@123"
    )

    response = client.post(
        "/login",
        data={
            "username": "testuser@gmail.com",
            "password": "Test@123"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password():

    create_test_user(
        "Wrong Password User",
        "wrongpassword@test.com",
        "Test@123"
    )

    response = client.post(
        "/login",
        data={
            "username": "wrongpassword@test.com",
            "password": "WrongPassword"
        }
    )

    assert response.status_code == 401


def test_login_non_existing_user():

    response = client.post(
        "/login",
        data={
            "username": "doesnotexist@gmail.com",
            "password": "Test@123"
        }
    )

    assert response.status_code == 401


def test_login_without_credentials():

    response = client.post(
        "/login",
        data={}
    )

    assert response.status_code == 422