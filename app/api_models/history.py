from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime
from enum import Enum

class EntityType(str, Enum):
    PROJECT = 'project'
    TICKET = 'ticket'

class ChangeType(str, Enum):
    STATUS_CHANGE = 'status_change'
    PRIORITY_CHANGE = 'priority_change'
    COMMENT_CHANGE = 'comment_change'
    CREATE = 'create'
    UPDATE = 'update'
    DELETE = 'delete'

class HistoryCreate(BaseModel):
    entity_type: EntityType
    entity_id: int
    change_type: ChangeType
    user_id: int
    details: Optional[str] = None

    @field_validator('details')
    def details_not_empty(cls, v, info):
        change_type = info.data.get('change_type')
        if change_type is None:
            raise ValueError('change_type must be provided')
        if change_type == ChangeType.COMMENT_CHANGE and not v:
            raise ValueError('details must be provided for comments')
        return v

class HistoryUpdate(BaseModel):
    entity_type: EntityType
    entity_id: int
    change_type: ChangeType
    user_id: int
    details: Optional[str] = None

    @field_validator('details')
    def details_not_empty(cls, v, info):
        change_type = info.data.get('change_type')
        if change_type is None:
            raise ValueError('change_type must be provided')
        if change_type == ChangeType.COMMENT_CHANGE and not v:
            raise ValueError('details must be provided for comments')
        return v

class HistoryResponse(HistoryCreate):
    id: int
    timestamp: datetime
    
    class Config:
        from_attributes = True