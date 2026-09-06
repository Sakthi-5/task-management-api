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