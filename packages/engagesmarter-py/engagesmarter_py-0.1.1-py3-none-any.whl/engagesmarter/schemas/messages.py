from datetime import datetime
from typing import Literal

from pydantic import BaseModel


class MessageRead(BaseModel):
    """A message via the Engage Smarter API"""

    id: str
    org_id: str
    conversation_id: str
    run_id: str
    role: str
    content: str
    created: datetime
    name: str | None = None
    user_id: str | None = None


class MessageBasic(BaseModel):
    """A message with just the basic fields"""

    role: str
    content: str
    name: str | None = None


class UserMessage(MessageBasic):
    """Message from a user"""

    role: Literal["user"] = "user"
    content: str
    name: str | None = None


class AgentMessage(MessageBasic):
    """Message from an agent to the user"""

    role: Literal["agent"] = "agent"
    content: str
    name: str | None = None


class InfoMessage(MessageBasic):
    """Message created by an agent that provides additional metadata"""

    role: Literal["info"] = "info"
    content: str
    name: str | None = None


class StatusMessage(MessageBasic):
    """Message from an agent that is emitted during an API call that provides a status update to the user."""

    role: Literal["status"] = "status"
    content: str
    name: str | None = None
