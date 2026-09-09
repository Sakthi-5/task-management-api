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


def test_create_task_without_token():
    response = client.post(
        "/tasks",
        json={
            "title": "DSA",
            "description": "Complete sliding window",
            "status": "pending"
        }
    )

    assert response.status_code == 401


def test_create_task_with_token():

    create_test_user(
        "Task User",
        "taskuser@test.com",
        "Test@123"
    )

    token = login_user(
        "taskuser@test.com",
        "Test@123"
    )

    response = client.post(
        "/tasks",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "title": "DSA",
            "description": "Complete sliding window",
            "status": "pending"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["title"] == "DSA"
    assert data["user_id"] > 0


def test_get_tasks_without_token():

    response = client.get("/tasks")

    assert response.status_code == 401


def test_get_tasks_with_token():

    create_test_user(
        "Task User 2",
        "taskuser2@test.com",
        "Test@123"
    )

    token = login_user(
        "taskuser2@test.com",
        "Test@123"
    )

    response = client.get(
        "/tasks",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200


def test_get_task_by_id_without_token():

    response = client.get("/tasks/1")

    assert response.status_code == 401


def test_get_user_tasks_without_token():

    response = client.get("/users/1/tasks")

    assert response.status_code == 401


def test_get_other_users_task_forbidden():

    create_test_user(
        "Owner User",
        "owner@test.com",
        "Test@123"
    )

    owner_token = login_user(
        "owner@test.com",
        "Test@123"
    )

    response = client.post(
        "/tasks",
        headers={
            "Authorization": f"Bearer {owner_token}"
        },
        json={
            "title": "Owner Task",
            "description": "Private task",
            "status": "pending"
        }
    )

    assert response.status_code == 200

    task_id = response.json()["id"]

    create_test_user(
        "Other User",
        "other@test.com",
        "Test@123"
    )

    other_token = login_user(
        "other@test.com",
        "Test@123"
    )

    response = client.get(
        f"/tasks/{task_id}",
        headers={
            "Authorization": f"Bearer {other_token}"
        }
    )

    assert response.status_code == 403


def test_get_other_users_tasks_forbidden():

    owner_response = create_test_user(
        "Task Owner",
        "taskowner@test.com",
        "Test@123"
    )

    owner_id = owner_response.json()["id"]

    owner_token = login_user(
        "taskowner@test.com",
        "Test@123"
    )

    response = client.post(
        "/tasks",
        headers={
            "Authorization": f"Bearer {owner_token}"
        },
        json={
            "title": "Private Task",
            "description": "Owner task",
            "status": "pending"
        }
    )

    assert response.status_code == 200

    create_test_user(
        "Another User",
        "another@test.com",
        "Test@123"
    )

    another_token = login_user(
        "another@test.com",
        "Test@123"
    )

    response = client.get(
        f"/users/{owner_id}/tasks",
        headers={
            "Authorization": f"Bearer {another_token}"
        }
    )

    assert response.status_code == 403


def test_update_other_users_task_forbidden():

    create_test_user(
        "Task Owner",
        "putowner@test.com",
        "Test@123"
    )

    owner_token = login_user(
        "putowner@test.com",
        "Test@123"
    )

    response = client.post(
        "/tasks",
        headers={
            "Authorization": f"Bearer {owner_token}"
        },
        json={
            "title": "Original Task",
            "description": "Original description",
            "status": "pending"
        }
    )

    assert response.status_code == 200

    task_id = response.json()["id"]

    create_test_user(
        "Other User",
        "putother@test.com",
        "Test@123"
    )

    other_token = login_user(
        "putother@test.com",
        "Test@123"
    )

    response = client.put(
        f"/tasks/{task_id}",
        headers={
            "Authorization": f"Bearer {other_token}"
        },
        json={
            "title": "Hacked Task",
            "description": "Trying to modify another user's task",
            "status": "completed"
        }
    )

    assert response.status_code == 403


def test_delete_other_users_task_forbidden():

    create_test_user(
        "Delete Owner",
        "deleteowner@test.com",
        "Test@123"
    )

    owner_token = login_user(
        "deleteowner@test.com",
        "Test@123"
    )

    response = client.post(
        "/tasks",
        headers={
            "Authorization": f"Bearer {owner_token}"
        },
        json={
            "title": "Task To Protect",
            "description": "Another user should not delete this",
            "status": "pending"
        }
    )

    assert response.status_code == 200

    task_id = response.json()["id"]

    create_test_user(
        "Delete Other User",
        "deleteother@test.com",
        "Test@123"
    )

    other_token = login_user(
        "deleteother@test.com",
        "Test@123"
    )

    response = client.delete(
        f"/tasks/{task_id}",
        headers={
            "Authorization": f"Bearer {other_token}"
        }
    )

    assert response.status_code == 403