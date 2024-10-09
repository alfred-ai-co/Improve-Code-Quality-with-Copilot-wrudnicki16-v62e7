from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
import datetime
from .base import Base

class KanbanStatus(Base):
    """
    Represents a status in a Kanban board.
    """
    __tablename__ = "kanban_statuses"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    tickets = relationship("Ticket", back_populates="kanban_status")