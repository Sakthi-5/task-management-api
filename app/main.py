from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.auth.dependencies import get_current_user
from app.auth.security import create_access_token
from app.schemas.auth import LoginRequest
from app.services.auth_service import authenticate_user
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
        email=user.email,
        password=user.password
    )

    return {
        "id": new_user.id,
        "name": new_user.name,
        "email": new_user.email
    }

@app.get("/users")
def get_users(
    current_user=Depends(get_current_user)
):
    user = get_user_by_id(current_user.id)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {
        "id": user.id,
        "name": user.name,
        "email": user.email
    }

@app.get("/users/{user_id}")
def get_user(
    user_id: int,
    current_user=Depends(get_current_user)
):
    if user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You are not authorized to access this user"
        )

    user = get_user_by_id(user_id)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {
        "id": user.id,
        "name": user.name,
        "email": user.email
    }
@app.put("/users/{user_id}")
def update_user_details(
    user_id: int,
    user: UserCreate,
    current_user=Depends(get_current_user)
):
    if user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You are not authorized to update this user"
        )

    updated_user = update_user(
        user_id=user_id,
        name=user.name,
        email=user.email
    )

    if updated_user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {
        "id": updated_user.id,
        "name": updated_user.name,
        "email": updated_user.email
    }
@app.delete("/users/{user_id}")
def remove_user(
    user_id: int,
    current_user=Depends(get_current_user)
):
    if user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You are not authorized to delete this user"
        )

    deleted_user = delete_user(user_id)

    if deleted_user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {
        "message": "User deleted successfully",
        "id": deleted_user.id,
        "name": deleted_user.name,
        "email": deleted_user.email
    }

@app.post("/tasks")
def add_task(
    task: TaskCreate,
    current_user=Depends(get_current_user)
):
    new_task = create_task(
        title=task.title,
        description=task.description,
        status=task.status,
        user_id=current_user.id
    )

    if new_task == "user_not_found":
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {
        "id": new_task.id,
        "title": new_task.title,
        "description": new_task.description,
        "status": new_task.status,
        "user_id": new_task.user_id
    }
@app.get("/tasks")
def get_tasks(
    current_user=Depends(get_current_user)
):
    all_tasks = get_all_tasks()

    user_tasks = [
        task
        for task in all_tasks
        if task.user_id == current_user.id
    ]

    return [
        {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "status": task.status,
            "user_id": task.user_id
        }
        for task in user_tasks
    ]
@app.get("/tasks/{task_id}")
def get_task(
    task_id: int,
    current_user=Depends(get_current_user)
):
    task = get_task_by_id(task_id)

    if task == "task_not_found":
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    if task.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You are not authorized to access this task"
        )

    return {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "status": task.status,
        "user_id": task.user_id
    }
@app.get("/users/{user_id}/tasks")
def get_user_tasks(
    user_id: int,
    current_user=Depends(get_current_user)
):

    if user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You are not authorized to access these tasks"
        )

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
def edit_task(
    task_id: int,
    task: TaskUpdate,
    current_user=Depends(get_current_user)
):
    existing_task = get_task_by_id(task_id)

    if existing_task == "task_not_found":
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    if existing_task.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You are not authorized to modify this task"
        )

    updated_task = update_task(
        task_id=task_id,
        title=task.title,
        description=task.description,
        status=task.status,
        user_id=current_user.id
    )

    return {
        "id": updated_task.id,
        "title": updated_task.title,
        "description": updated_task.description,
        "status": updated_task.status,
        "user_id": updated_task.user_id
    }
@app.delete("/tasks/{task_id}")
def remove_task(
    task_id: int,
    current_user=Depends(get_current_user)
):
    existing_task = get_task_by_id(task_id)

    if existing_task == "task_not_found":
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    if existing_task.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You are not authorized to delete this task"
        )

    deleted_task = delete_task(task_id)

    return {
        "message": "Task deleted successfully",
        "id": deleted_task.id
    }
@app.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends()
):

    user = authenticate_user(
        email=form_data.username,
        password=form_data.password
    )

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    access_token = create_access_token(user.id)

    return {
        "message": "Login successful",
        "access_token": access_token,
        "token_type": "bearer"
    }