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


def login_user(email, password):
    response = client.post(
        "/login",
        data={
            "username": email,
            "password": password
        }
    )

    assert response.status_code == 200

    return response.json()["access_token"]


def test_create_user():

    response = create_test_user(
        "Test User",
        "testuser@test.com",
        "Test@123"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "Test User"
    assert data["email"] == "testuser@test.com"
    assert "id" in data


def test_get_users():

    create_response = create_test_user(
        "Get User",
        "getuser@test.com",
        "Test@123"
    )

    user_id = create_response.json()["id"]

    token = login_user(
        "getuser@test.com",
        "Test@123"
    )

    response = client.get(
        "/users",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == user_id
    assert data["name"] == "Get User"
    assert data["email"] == "getuser@test.com"


def test_get_user_by_id():

    create_response = create_test_user(
        "Single User",
        "singleuser@test.com",
        "Test@123"
    )

    user_id = create_response.json()["id"]

    token = login_user(
        "singleuser@test.com",
        "Test@123"
    )

    response = client.get(
        f"/users/{user_id}",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == user_id
    assert data["email"] == "singleuser@test.com"


def test_update_own_user():

    create_response = create_test_user(
        "Update User",
        "updateuser@test.com",
        "Test@123"
    )

    user_id = create_response.json()["id"]

    token = login_user(
        "updateuser@test.com",
        "Test@123"
    )

    response = client.put(
        f"/users/{user_id}",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "name": "Updated User",
            "email": "updateduser@test.com",
            "password": "Test@123"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == user_id
    assert data["name"] == "Updated User"
    assert data["email"] == "updateduser@test.com"


def test_delete_other_user_forbidden():

    user1_response = create_test_user(
        "Delete User One",
        "deleteuser1@test.com",
        "Test@123"
    )

    user1_id = user1_response.json()["id"]

    create_test_user(
        "Delete User Two",
        "deleteuser2@test.com",
        "Test@123"
    )

    user2_token = login_user(
        "deleteuser2@test.com",
        "Test@123"
    )

    response = client.delete(
        f"/users/{user1_id}",
        headers={
            "Authorization": f"Bearer {user2_token}"
        }
    )

    assert response.status_code == 403