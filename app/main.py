from fastapi import FastAPI
from app.schemas.user import UserCreate
from app.services.user_service import create_user, get_all_users
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