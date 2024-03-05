from importlib import metadata

try:
    __version__ = metadata.version(__package__)
except metadata.PackageNotFoundError:
    # Case where package metadata is not available.
    __version__ = ""

from .client import Client
from .schemas.agents import AgentMetadata
from .schemas.base import Success
from .schemas.conversations import (
    ConversationCreate,
    ConversationRead,
    ConversationUpdate,
)
from .schemas.feedback import FeedbackRead, FeedbackUpsert
from .schemas.messages import (
    AgentMessage,
    InfoMessage,
    MessageBasic,
    MessageRead,
    StatusMessage,
    UserMessage,
)
from .schemas.runs import RunRead
from .schemas.tags import TagCreate, TagRead, TagUpdate

__all__ = [
    Client,
    AgentMessage,
    AgentMetadata,
    ConversationCreate,
    ConversationRead,
    ConversationUpdate,
    FeedbackRead,
    FeedbackUpsert,
    MessageBasic,
    MessageRead,
    RunRead,
    Success,
    TagCreate,
    TagRead,
    TagUpdate,
    UserMessage,
    InfoMessage,
    StatusMessage,
    __version__,
]
