from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
import datetime
from .base import Base

class Ticket(Base):
    __tablename__ = "tickets"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    status = Column(String(255), nullable=False)
    priority = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    kanban_status_id = Column(Integer, ForeignKey("kanban_statuses.id"), nullable=False)
    
    project = relationship("Project", back_populates="tickets")
    kanban_status = relationship('KanbanStatus', back_populates='tickets')