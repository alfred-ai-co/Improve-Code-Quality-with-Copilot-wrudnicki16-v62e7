from sqlalchemy.orm import Session
from ..kanban_status import KanbanStatus
from .base import BaseCRUD

class CRUDKanbanStatus(BaseCRUD[KanbanStatus]):
    pass

ticket = CRUDKanbanStatus(KanbanStatus)