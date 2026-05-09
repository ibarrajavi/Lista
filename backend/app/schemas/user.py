# --- Third-party
from pydantic import BaseModel, ConfigDict, EmailStr, field_validator

# --- Standard library
import re
from uuid import UUID


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: EmailStr
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < 12:
            raise ValueError("Password must be at least 12 characters")
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r"[!@#$%^&*]", v):
            raise ValueError("Password must contain at least one special character (!@#$%^&*)")
        if len(re.findall(r"\d", v)) < 2:
            raise ValueError("Password must contain at least two numbers")
        if re.search(r"\s", v):
            raise ValueError("Password must not contain whitespace")
        return v


class UserCreateResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    username: str
    email: str
    first_name: str
    last_name: str
