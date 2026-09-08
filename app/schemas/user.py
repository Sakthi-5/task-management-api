from pydantic import BaseModel, EmailStr, field_validator

from app.utils.validators import validate_not_empty


class UserCreate(BaseModel):
    name: str
    email: EmailStr

    @field_validator("name")
    @classmethod
    def check_name(cls, value):
        if not validate_not_empty(value):
            raise ValueError("Name cannot be empty")
        return value.strip()