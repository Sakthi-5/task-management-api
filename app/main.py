from fastapi import FastAPI
from app.schemas.user import UserCreate
from app.services.user_service import create_user, get_all_users, get_user_by_id,update_user,delete_user

from app.config import APP_NAME

app = FastAPI(title=APP_NAME)


@app.get("/")
def home():
    return {"message": "Welcome to the Task Management API"}


@app.post("/users")
def add_user(user: UserCreate):
    new_user = create_user(
        name=user.name,
        email=user.email
    )

    return {
        "id": new_user.id,
        "name": new_user.name,
        "email": new_user.email
    }


@app.get("/users")
def get_users():
    all_users = get_all_users()

    return [
        {
            "id": user.id,
            "name": user.name,
            "email": user.email
        }
        for user in all_users
    ]


@app.get("/users/{user_id}")
def get_user(user_id: int):
    user = get_user_by_id(user_id)

    if user is None:
        return {"message": "User not found"}

    return {
        "id": user.id,
        "name": user.name,
        "email": user.email
    }
@app.put("/users/{user_id}")
def update_user_details(user_id: int, user: UserCreate):
    updated_user = update_user(
        user_id=user_id,
        name=user.name,
        email=user.email
    )

    if updated_user is None:
        return {"message": "User not found"}

    return {
        "id": updated_user.id,
        "name": updated_user.name,
        "email": updated_user.email
    }
@app.delete("/users/{user_id}")
def remove_user(user_id: int):
    deleted_user = delete_user(user_id)

    if deleted_user is None:
        return {"message": "User not found"}

    return {
        "message": "User deleted successfully",
        "id": deleted_user.id,
        "name": deleted_user.name,
        "email": deleted_user.email
    }