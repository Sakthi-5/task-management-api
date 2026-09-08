from app.models.task import Task
from app.services.user_service import get_user_by_id


tasks = []


def create_task(title: str, description: str, status: str, user_id: int):
    user = get_user_by_id(user_id)

    if user is None:
        return "user_not_found"

    task_id = len(tasks) + 1

    new_task = Task(
        task_id=task_id,
        title=title,
        description=description,
        status=status,
        user_id=user_id
    )

    tasks.append(new_task)

    return new_task


def get_all_tasks():
    return tasks


def get_task_by_id(task_id: int):
    for task in tasks:
        if task.id == task_id:
            return task

    return "task_not_found"


def get_tasks_by_user_id(user_id: int):
    user = get_user_by_id(user_id)

    if user is None:
        return "user_not_found"

    user_tasks = []

    for task in tasks:
        if task.user_id == user_id:
            user_tasks.append(task)

    return user_tasks


def update_task(
    task_id: int,
    title: str,
    description: str,
    status: str,
    user_id: int
):
    user = get_user_by_id(user_id)

    if user is None:
        return "user_not_found"

    for task in tasks:
        if task.id == task_id:
            task.title = title
            task.description = description
            task.status = status
            task.user_id = user_id
            return task

    return "task_not_found"


def delete_task(task_id: int):
    for task in tasks:
        if task.id == task_id:
            tasks.remove(task)
            return task

    return "task_not_found"