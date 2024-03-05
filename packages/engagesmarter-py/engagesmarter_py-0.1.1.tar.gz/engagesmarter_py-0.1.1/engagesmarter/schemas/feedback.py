from datetime import datetime
from typing import Literal

from pydantic import BaseModel


class FeedbackRead(BaseModel):
    id: str
    org_id: str
    conversation_id: str
    run_id: str
    user_id: str
    thumbs: Literal["up", "down", ""]
    comment: str
    created: datetime


class FeedbackUpsert(BaseModel):
    thumbs: Literal["up", "down", ""] = ""
    comment: str = ""
