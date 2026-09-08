from app.schemas.task import TaskCreate,TaskUpdate 
from app.services.task_service import create_task,get_all_tasks,get_task_by_id,get_tasks_by_user_id,update_task,delete_task
from fastapi import FastAPI, HTTPException
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

@app.post("/tasks")
def add_task(task: TaskCreate):
    new_task = create_task(
        title=task.title,
        description=task.description,
        status=task.status,
        user_id=task.user_id
    )

    if new_task == "user_not_found":
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "id": new_task.id,
        "title": new_task.title,
        "description": new_task.description,
        "status": new_task.status,
        "user_id": new_task.user_id
    }
@app.get("/tasks")
def get_tasks():
    all_tasks = get_all_tasks()

    return [
        {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "status": task.status,
            "user_id": task.user_id
        }
        for task in all_tasks
    ]
@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    task = get_task_by_id(task_id)

    if task == "task_not_found":
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "status": task.status,
        "user_id": task.user_id
    }
@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    task = get_task_by_id(task_id)

    if task == "task_not_found":
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "status": task.status,
        "user_id": task.user_id
    }
@app.get("/users/{user_id}/tasks")
def get_user_tasks(user_id: int):

    user_tasks = get_tasks_by_user_id(user_id)

    if user_tasks == "user_not_found":
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return [
        {
            "sequence": index + 1,
            "task_id": task.id,
            "title": task.title,
            "description": task.description,
            "status": task.status,
            "user_id": task.user_id
        }
        for index, task in enumerate(user_tasks)
    ]
@app.put("/tasks/{task_id}")
def edit_task(task_id: int, task: TaskUpdate):
    updated_task = update_task(
        task_id=task_id,
        title=task.title,
        description=task.description,
        status=task.status,
        user_id=task.user_id
    )

    if updated_task == "user_not_found":
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if updated_task == "task_not_found":
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return {
        "id": updated_task.id,
        "title": updated_task.title,
        "description": updated_task.description,
        "status": updated_task.status,
        "user_id": updated_task.user_id
    }
@app.delete("/tasks/{task_id}")
def remove_task(task_id: int):
    deleted_task = delete_task(task_id)

    if deleted_task is None:
        return {"message": "Task not found"}

    return {
        "message": "Task deleted successfully",
        "id": deleted_task.id
    }