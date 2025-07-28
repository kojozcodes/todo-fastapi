from pydantic import BaseModel, Field
from uuid import uuid4
from datetime import datetime
from typing import Optional

class TodoCreate(BaseModel):
    title: str = Field(..., min_length=1)
    description: Optional[str] = None

class Todo(TodoCreate):
    id: str
    completed: bool = False
    timestamp: datetime

class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None