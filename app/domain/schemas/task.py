from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    priority: Optional[int] = 1

    class Config:
        from_attributes = True


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[int] = None
    completed: Optional[bool] = None

    class Config:
        from_attributes = True


class TaskOut(BaseModel):
    id: int
    title: str
    description: Optional[str]
    priority: int
    completed: bool
    created_at: datetime

    class Config:
        from_attributes = True


class TaskListCreate(BaseModel):
    name: str


class TaskListOut(BaseModel):
    id: int
    name: str
    created_at: datetime
    tasks: List["TaskOut"] = []
    completed_percentage: float = 0.0

    class Config:
        from_attributes = True
