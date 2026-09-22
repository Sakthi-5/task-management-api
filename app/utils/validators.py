def validate_task_status(status: str):
    allowed_statuses = ["pending", "in_progress", "completed"]

    if status not in allowed_statuses:
        return False

    return True


def validate_not_empty(value: str):
    if not value or not value.strip():
        return False

    return True