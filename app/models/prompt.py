from pydantic import BaseModel
from datetime import datetime

class PromptCreate(BaseModel):
    name: str
    content: str
    description: str | None = None

class PromptRead(BaseModel):
    id: int
    name: str
    content: str
    description: str | None = None
    created_at: datetime