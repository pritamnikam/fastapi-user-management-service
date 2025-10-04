from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class PromptCreate(BaseModel):
    app_id: str
    prompt_key: str
    prompt_text: str
    version: int = Field(default=1)
    is_active: bool = Field(default=False)
    created_by: str

class PromptRead(BaseModel):
    id: int
    app_id: str
    prompt_key: str
    prompt_text: str
    version: int
    is_active: bool
    created_by: str
    created_at: datetime

class PromptUpdate(BaseModel):
    prompt_text: Optional[str] = None
    is_active: Optional[bool] = None