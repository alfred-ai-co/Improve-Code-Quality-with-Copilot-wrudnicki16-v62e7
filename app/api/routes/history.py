from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from typing import List
from sqlalchemy.orm import Session
from app.api.dependencies.sqldb import get_db
from app.db_models.crud import HistoryCRUD
from app.api_models.history import HistoryCreate, HistoryUpdate, HistoryResponse

router = APIRouter()

@router.post("/", response_model=HistoryResponse)
def create_history(history: HistoryCreate, db: Session = Depends(get_db)):
    history_crud = HistoryCRUD(db)
    return history_crud.create(**history.model_dump())

@router.get("/{entity_id}", response_model=List[HistoryResponse])
def get_history_by_entity_id(entity_type: str, entity_id: int, offset: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    history_crud = HistoryCRUD(db)

    # Apply this if history retrieval becomes too slow
    # total_records = history_crud.count_by_entity_id(entity_id)

    # if total_records > 10000:
    #     if background_tasks:
    #         background_tasks.add_task(history_crud.retrieve_history_records, entity_id, offset, limit)
    #     return {"message": "History retrieval task started in the background, ask users to refresh to access records later."}

    return history_crud.get_by_entity_id(entity_type, entity_id, offset=offset, limit=limit)

@router.put("/{id}", response_model=HistoryResponse)
def update_history(id: int, history: HistoryUpdate, db: Session = Depends(get_db)):
    history_crud = HistoryCRUD(db)
    db_history = history_crud.get(id)
    if not db_history:
        raise HTTPException(status_code=404, detail="History not found")
    return history_crud.update(id, **history.model_dump())

@router.delete("/{id}", response_model=HistoryResponse)
def delete_history(id: int, db: Session = Depends(get_db)):
    history_crud = HistoryCRUD(db)
    db_history = history_crud.get(id)
    if not db_history:
        raise HTTPException(status_code=404, detail="History not found")
    history_crud.delete(id)
    return db_history