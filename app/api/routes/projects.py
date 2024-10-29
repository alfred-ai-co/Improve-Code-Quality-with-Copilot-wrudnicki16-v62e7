# Project Endpoints
from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from fastapi import Depends

from app.db_models.crud import ProjectCRUD
from app.api_models.projects import ProjectCreate, ProjectResponse
from app.api.dependencies.sqldb import get_db
from app.api.routes.history import get_history_by_entity_id
from app.api_models.projects import ProjectWithHistory


router = APIRouter()


@router.post("/", status_code=201, response_model=ProjectResponse)
def create_project(project: ProjectCreate, db: Session = Depends(get_db)):
    project_crud = ProjectCRUD(db)
    return project_crud.create(**project.model_dump())


@router.get("/", status_code=200, response_model=list[ProjectResponse])
def get_all_projects(db: Session = Depends(get_db)):
    project_crud = ProjectCRUD(db)
    return project_crud.get_all()


@router.get("/{id}", status_code=200, response_model=ProjectResponse)
def get_project(id: int, db: Session = Depends(get_db)):
    project_crud = ProjectCRUD(db)
    project = project_crud.get(id)
    if not project:
        raise HTTPException(status_code=404, detail=f"Project with id {id} not found")
    return project

@router.get("/{project_id}", response_model=ProjectWithHistory)
async def get_project_with_history(project_id: int, db: Session = Depends(get_db)):
    project_crud = ProjectCRUD(db)
    project = project_crud.get(project_id)
    if not project:
        raise HTTPException(status_code=404, detail=f"Ticket with id {project_id} not found")
    history = await get_history_by_entity_id('project', project_id, db=db)
    return ProjectWithHistory(project=project, history=history)

@router.put("/{id}", status_code=200, response_model=ProjectResponse)
def update_project(id: int, project: ProjectCreate, db: Session = Depends(get_db)):
    project_crud = ProjectCRUD(db)
    project_crud.update(id, **project.model_dump())
    return project_crud.get(id)


@router.delete("/{id}", status_code=204)
def delete_project(id: int, db: Session = Depends(get_db)):
    project_crud = ProjectCRUD(db)
    project_crud.delete(id)
    return {"message": "Project deleted successfully"}

