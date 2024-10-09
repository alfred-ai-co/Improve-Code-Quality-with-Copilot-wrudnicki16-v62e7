from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None
    kanban_board_id: int


class ProjectResponse(ProjectCreate):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

