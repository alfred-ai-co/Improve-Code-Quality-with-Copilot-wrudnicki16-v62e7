from sqlalchemy import event
from sqlalchemy.orm import Session
from app.db_models.base import Project, Ticket, History
from app.api.dependencies.sqldb import get_db
import datetime

def create_history_entry(mapper, connection, target):
    # Use the get_db dependency to create a session
    db_gen = get_db()
    session = next(db_gen)
    
    if session is None:
        return

    if isinstance(target, Project):
        entity_type = 'project'
        entity_id = target.id
        change_type = 'status_change'
        old_status = session.query(Project).filter(Project.id == target.id).first().status
        new_status = target.status
        if old_status == new_status:
            return
        details = f"Status changed from {old_status} to {new_status}"
    elif isinstance(target, Ticket):
        entity_type = 'ticket'
        entity_id = target.id
        change_type = 'status_change'
        old_status = session.query(Ticket).filter(Ticket.id == target.id).first().status
        new_status = target.status
        if old_status == new_status:
            return
        details = f"Status changed from {old_status} to {new_status}"
    else:
        return

    history_entry = History(
        entity_type=entity_type,
        entity_id=entity_id,
        change_type=change_type,
        timestamp=datetime.datetime.now(datetime.timezone.utc),
        user_id=1,  # Replace with actual user ID
        details=details
    )
    session.add(history_entry)
    session.commit()
    
    # Close the session
    session.close()

# Attach the event listeners
event.listen(Project, 'before_update', create_history_entry)
event.listen(Ticket, 'before_update', create_history_entry)