from fastapi import FastAPI
from app.schemas.user import UserCreate
from app.services.user_service import create_user
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