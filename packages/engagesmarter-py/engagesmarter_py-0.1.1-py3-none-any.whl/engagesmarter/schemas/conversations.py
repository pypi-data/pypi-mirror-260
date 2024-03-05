from datetime import datetime

from pydantic import BaseModel


class ConversationRead(BaseModel):
    id: str
    org_id: str
    data: dict
    cloned_from_message_id: str | None
    created: datetime


class ConversationUpdate(BaseModel):
    data: dict | None = None


class ConversationCreate(BaseModel):
    data: dict = {}
