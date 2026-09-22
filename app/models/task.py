class Task:
    def __init__(
        self,
        task_id: int,
        title: str,
        description: str,
        status: str,
        user_id: int
    ):
        self.id = task_id
        self.title = title
        self.description = description
        self.status = status
        self.user_id = user_id