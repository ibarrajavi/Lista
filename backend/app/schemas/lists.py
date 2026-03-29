from pydantic import BaseModel, ConfigDict
from datetime import datetime

class ListCreateRequest(BaseModel):
    name: str = "New list"

class ListResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    name: str
    created_at: datetime

