import os
from unittest import mock

import pytest

from client.engagesmarter import Client
from client.engagesmarter.resources.agents import AgentsResource
from client.engagesmarter.resources.conversations import ConversationsResource
from client.engagesmarter.resources.runs import RunsResource
from client.engagesmarter.resources.tags import TagsResource


@pytest.fixture
def api_key() -> str:
    """API key."""
    return "API_KEY"


@pytest.fixture
def org_id() -> str:
    """Org ID."""
    return "ORG_ID"


@pytest.fixture
def custom_api_url() -> str:
    """Custom API URL."""
    return "http://localhost:1234"


@pytest.fixture
def local_api_url() -> str:
    """Localhost API URL."""
    return os.getenv("API_URL")


@pytest.fixture
def mock_httpx_client():
    return mock.Mock()


@pytest.fixture
def mock_engagesmarter_client() -> Client:
    """Client pointing at mock API."""
    return Client(
        api_key="API_KEY",
        org_id="ORG_ID",
        api_url="http://not_a_real_url",
    )


@pytest.fixture
def local_engagesmarter_client() -> Client:
    """Client pointing at locally hosted API."""
    return Client(
        api_url=os.getenv("API_URL"),
        api_key=os.getenv("ENGAGE_SMARTER_API_KEY"),
        org_id=os.getenv("ENGAGE_SMARTER_ORG_ID"),
    )


@pytest.fixture
def agents(
    local_engagesmarter_client: Client,
) -> AgentsResource:
    """Agents resource pointing at locally hosted API."""
    return local_engagesmarter_client.agents


@pytest.fixture
def conversations(
    local_engagesmarter_client: Client,
) -> ConversationsResource:
    """Conversations resource pointing at locally hosted API."""
    return local_engagesmarter_client.conversations


@pytest.fixture
def runs(
    local_engagesmarter_client: Client,
) -> RunsResource:
    """Runs resource pointing at locally hosted API."""
    return local_engagesmarter_client.runs


@pytest.fixture
def tags(
    local_engagesmarter_client: Client,
) -> TagsResource:
    """Tags resource pointing at locally hosted API."""
    return local_engagesmarter_client.tags
