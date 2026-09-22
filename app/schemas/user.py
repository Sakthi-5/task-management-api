from pydantic import BaseModel, EmailStr, field_validator

from app.utils.validators import validate_not_empty


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

    @field_validator("name", "password")
    @classmethod
    def check_required_fields(cls, value):
        if not validate_not_empty(value):
            raise ValueError("Field cannot be empty")
        return value.strip()