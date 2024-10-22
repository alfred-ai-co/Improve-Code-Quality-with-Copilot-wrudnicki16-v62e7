from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import datetime


Base = declarative_base()


class Project(Base):
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc), onupdate=lambda: datetime.datetime.now(datetime.timezone.utc))
    kanban_board_id = Column(Integer, ForeignKey("kanban_boards.id"), nullable=False)
    
    kanban_board = relationship("KanbanBoard", back_populates="projects")
    tickets = relationship("Ticket", back_populates="project")
    history = relationship("History", back_populates="project", foreign_keys="[History.project_id]")

class Ticket(Base):
    __tablename__ = "tickets"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    status = Column(String(255), nullable=False)
    priority = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc), onupdate=lambda: datetime.datetime.now(datetime.timezone.utc))
    kanban_status_id = Column(Integer, ForeignKey("kanban_statuses.id"), nullable=False)
    
    project = relationship("Project", back_populates="tickets")
    kanban_status = relationship('KanbanStatus', back_populates='tickets')
    history = relationship("History", back_populates="ticket", foreign_keys="[History.ticket_id]")


class KanbanBoard(Base):
    __tablename__ = "kanban_boards"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc), onupdate=lambda: datetime.datetime.now(datetime.timezone.utc))

    projects = relationship('Project', back_populates='kanban_board')
    statuses = relationship('KanbanStatus', back_populates='kanban_board')

class KanbanStatus(Base):
    __tablename__ = "kanban_statuses"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    board_id = Column(Integer, ForeignKey("kanban_boards.id"), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc), onupdate=lambda: datetime.datetime.now(datetime.timezone.utc))
    
    kanban_board = relationship('KanbanBoard', back_populates='statuses')
    tickets = relationship('Ticket', back_populates='kanban_status')

class History(Base):
    __tablename__ = 'history'

    id = Column(Integer, primary_key=True, index=True)
    entity_type = Column(String, nullable=False)
    entity_id = Column(Integer, nullable=False)
    change_type = Column(String, nullable=False)
    timestamp = Column(DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc))
    user_id = Column(Integer, nullable=False)
    details = Column(Text, nullable=True)
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=True)
    ticket_id = Column(Integer, ForeignKey('tickets.id'), nullable=True)

    project = relationship('Project', back_populates='history', foreign_keys=[project_id])
    ticket = relationship('Ticket', back_populates='history', foreign_keys=[ticket_id])
