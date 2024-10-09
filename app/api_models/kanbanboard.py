from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class KanbanBoardBase(BaseModel):
    name: str
    description: Optional[str] = None


class KanbanBoardCreate(KanbanBoardBase):
    pass


class KanbanBoardUpdate(KanbanBoardBase):
    pass


class KanbanBoardInDB(KanbanBoardBase):
    id: int
    created_at: datetime
    
    class Config:
        orm_mode = True


class KanbanBoardResponse(KanbanBoardInDB):
    pass
