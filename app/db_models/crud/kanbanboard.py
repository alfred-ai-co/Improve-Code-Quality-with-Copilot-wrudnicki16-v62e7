from sqlalchemy.orm import Session
from ..kanban_board import KanbanBoard
from .base import BaseCRUD

class CRUDKanbanBoard(BaseCRUD[KanbanBoard]):
    pass

ticket = CRUDKanbanBoard(KanbanBoard)