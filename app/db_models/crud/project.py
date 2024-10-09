from sqlalchemy.orm import Session
from ..project import Project
from .base import BaseCRUD

class CRUDProject(BaseCRUD[Project]):
    pass

project = CRUDProject(Project)