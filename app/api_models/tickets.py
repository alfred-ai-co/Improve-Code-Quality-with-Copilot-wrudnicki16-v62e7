from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from app.api_models.history import History


class TicketCreate(BaseModel):
    project_id: int
    title: str
    description: str
    status: str
    priority: str


class TicketResponse(TicketCreate):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class TicketWithHistory(BaseModel):
    ticket: TicketCreate
    history: List[History]