from fastapi import FastAPI
from loguru import logger
from typing import Callable, Optional
from sqlalchemy.orm import Session
from dotenv import load_dotenv, find_dotenv
import os

from app.db_models.base import *
from app.db_models.session import engine, SessionLocal

def create_default_statuses(db: Session) -> None:
    statuses = [
        KanbanStatus(name="Backlog", description="Backlog Status", board_id=1),
        KanbanStatus(name="To Do", description="To Do Status", board_id=1),
        KanbanStatus(name="In Progress", description="In Progress Status", board_id=1),
        KanbanStatus(name="Done", description="Done Status", board_id=1)
    ]
    db.add_all(statuses)
    db.commit()

def create_default_board(db: Session) -> None:
    board = KanbanBoard(name="Default Board", description="Default Kanban Board")
    db.add(board)
    db.commit()
    db.refresh(board)

def create_kanban_defaults(db: Session, create_defaults: Optional[str] = True) -> None:
    if create_defaults.lower() == 'true':
        logger.info("Creating default Kanban Board and Statuses")
        logger.info("To set off, add env variable CREATE_DEFAULTS=False")
        create_default_board(db)
        create_default_statuses(db)
    elif create_defaults.lower() == 'false': logger.info("Create defaults is set to False, not creating default Kanban Board and Statuses")
    else: logger.info("No CREATE_DEFAULTS env variable set, not creating default Kanban Board and Statuses")


def create_start_app_handler(app: FastAPI) -> Callable:
    async def start_app() -> None:
        settings = app.state.settings
        logger.info(f"Starting [{settings.app_env.value}] Application")
        # Start up Events
        load_dotenv(find_dotenv())
        
        # Create tables
        Base.metadata.create_all(bind=engine)
        
        # Create a new session
        session = SessionLocal()
        
        # Create default Kanban Board and Statuses
        create_kanban_defaults(session, os.getenv('CREATE_DEFAULTS'))
        
        # Close session
        session.close()
        
    return start_app

def create_stop_app_handler(app: FastAPI) -> Callable:
    @logger.catch
    async def stop_app() -> None:
        settings = app.state.settings
        logger.info(f"Stopping [{settings.app_env.value}] application")
        # Shut down events
    return stop_app
