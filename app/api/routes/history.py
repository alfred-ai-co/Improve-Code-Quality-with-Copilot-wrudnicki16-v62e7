from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from app.db_models.session import get_db
from app.db_models.crud import HistoryCRUD
from app.api_models.history import HistoryCreate, HistoryUpdate, HistoryResponse

router = APIRouter()

@router.post("/", response_model=HistoryResponse)
def create_history(history: HistoryCreate, db: Session = Depends(get_db)):
    crud = HistoryCRUD(db)
    return crud.create(**history.model_dump())

@router.get("/{entity_id}", response_model=List[HistoryResponse])
def get_history_by_entity_id(entity_id: int, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    crud = HistoryCRUD(db)
    return crud.get_by_entity_id(entity_id, skip=skip, limit=limit)

@router.put("/{id}", response_model=HistoryResponse)
def update_history(id: int, history: HistoryUpdate, db: Session = Depends(get_db)):
    crud = HistoryCRUD(db)
    db_history = crud.get(id)
    if not db_history:
        raise HTTPException(status_code=404, detail="History not found")
    return crud.update(id, **history.model_dump())

@router.delete("/{id}", response_model=HistoryResponse)
def delete_history(id: int, db: Session = Depends(get_db)):
    crud = HistoryCRUD(db)
    db_history = crud.get(id)
    if not db_history:
        raise HTTPException(status_code=404, detail="History not found")
    crud.delete(id)
    return db_history