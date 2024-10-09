from sqlalchemy.orm import Session
from ..ticket import Ticket
from .base import BaseCRUD

class CRUDTicket(BaseCRUD[Ticket]):
    pass

ticket = CRUDTicket(Ticket)