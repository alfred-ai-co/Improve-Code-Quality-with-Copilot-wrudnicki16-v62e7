# Project Endpoints
from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from fastapi import Depends

from app.db_models.crud import ProjectCRUD
from app.api_models.projects import ProjectCreate, ProjectResponse
from app.api.dependencies.sqldb import get_db


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

