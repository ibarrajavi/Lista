# --- Third-party
from pydantic import BaseModel, ConfigDict

# --- Standard library
from datetime import datetime
from uuid import UUID


class TaskCreateRequest(BaseModel):
    description: str


class TaskUpdateRequest(BaseModel):
    description: str | None = None
    position: int | None = None
    is_complete: bool | None = None


class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    list_id: UUID
    description: str
    position: int
    is_complete: bool
    created_at: datetime
    updated_at: datetime
