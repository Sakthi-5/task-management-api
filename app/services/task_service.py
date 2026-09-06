from app.models.task import Task

tasks = []
def create_task(title: str, description: str, status: str, user_id: int):
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

    return None
def update_task(task_id: int, title: str, description: str, status: str, user_id: int):
    for task in tasks:
        if task.id == task_id:
            task.title = title
            task.description = description
            task.status = status
            task.user_id = user_id
            return task

    return None
def delete_task(task_id: int):
    for task in tasks:
        if task.id == task_id:
            tasks.remove(task)
            return task

    return None