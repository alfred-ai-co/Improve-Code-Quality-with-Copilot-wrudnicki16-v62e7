from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from app.api_models.history import HistoryResponse


class TicketCreate(BaseModel):
    project_id: int
    title: str
    description: str
    status: str
    priority: str
    kanban_status_id: int


class TicketResponse(TicketCreate):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class TicketWithHistory(BaseModel):
    ticket: TicketResponse
    history: List[HistoryResponse]