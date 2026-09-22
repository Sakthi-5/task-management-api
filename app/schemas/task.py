from pydantic import BaseModel, field_validator

from app.utils.validators import validate_task_status, validate_not_empty


class TaskCreate(BaseModel):
    title: str
    description: str
    status: str

    @field_validator("title", "description")
    @classmethod
    def check_required_fields(cls, value):
        if not validate_not_empty(value):
            raise ValueError("Field cannot be empty")
        return value.strip()

    @field_validator("status")
    @classmethod
    def check_status(cls, value):
        if not validate_task_status(value):
            raise ValueError("Invalid task status")
        return value


class TaskUpdate(BaseModel):
    title: str
    description: str
    status: str

    @field_validator("title", "description")
    @classmethod
    def check_required_fields(cls, value):
        if not validate_not_empty(value):
            raise ValueError("Field cannot be empty")
        return value.strip()

    @field_validator("status")
    @classmethod
    def check_status(cls, value):
        if not validate_task_status(value):
            raise ValueError("Invalid task status")
        return value