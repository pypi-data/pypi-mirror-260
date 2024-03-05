from datetime import datetime

from pydantic import BaseModel


class RunRead(BaseModel):
    id: str
    org_id: str
    conversation_id: str
    agent: str
    test: bool
    created: datetime
