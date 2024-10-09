from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from fastapi import Depends

from app.db_models.crud import TicketCRUD
from app.api_models.tickets import TicketCreate, TicketResponse
from app.api.dependencies.sqldb import get_db


router = APIRouter()


@router.post("/", status_code=201, response_model=TicketResponse)
def create_ticket(ticket: TicketCreate, db: Session = Depends(get_db)):
    ticket_crud = TicketCRUD(db)
    return ticket_crud.create(**ticket.model_dump())


@router.get("/", status_code=200, response_model=list[TicketResponse])
def get_all_tickets(db: Session = Depends(get_db)):
    ticket_crud = TicketCRUD(db)
    return ticket_crud.get_all()


@router.get("/{id}", status_code=200, response_model=TicketResponse)
def get_ticket(id: int, db: Session = Depends(get_db)):
    ticket_crud = TicketCRUD(db)
    ticket = ticket_crud.get(id)
    if not ticket:
        raise HTTPException(status_code=404, detail=f"Ticket with id {id} not found")
    return ticket


@router.put("/{id}", status_code=200, response_model=TicketResponse)
def update_ticket(id: int, ticket: TicketCreate, db: Session = Depends(get_db)):
    ticket_crud = TicketCRUD(db)
    ticket_crud.update(id, **ticket.model_dump())
    return ticket_crud.get(id)


@router.delete("/{id}", status_code=204)
async def delete_ticket(id: int, db: Session = Depends(get_db)):
    ticket_crud = TicketCRUD(db)
    ticket_crud.delete(id)
    return {"message": "Ticket deleted successfully"}

