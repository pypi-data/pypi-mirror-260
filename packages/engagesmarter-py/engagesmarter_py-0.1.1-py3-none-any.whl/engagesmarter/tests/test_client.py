from unittest import mock

import httpx
import pytest
from pydantic import BaseModel

from client.engagesmarter import Client, constants, errors, resources
from client.engagesmarter.utils.pydantic import model_json


def test_client_init(
    api_key: str, org_id: str, custom_api_url: str, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Test Client init."""
    monkeypatch.delenv("ENGAGE_SMARTER_API_KEY", raising=False)
    monkeypatch.delenv("ENGAGE_SMARTER_ORG_ID", raising=False)
    monkeypatch.delenv("ENGAGE_SMARTER_API_URL", raising=False)
    with pytest.raises(errors.EngageSmarterError):
        client = Client()
    with pytest.raises(errors.EngageSmarterError):
        client = Client(api_url=custom_api_url)
    with pytest.raises(errors.EngageSmarterError):
        client = Client(api_key=api_key)
    with pytest.raises(errors.EngageSmarterError):
        client = Client(org_id=org_id)

    with pytest.raises(TypeError):
        client = Client(api_key, org_id)

    client = Client(api_key=api_key, org_id=org_id)
    assert client is not None
    assert client._client.api_url == constants.DEFAULT_API_URL

    monkeypatch.setenv("ENGAGE_SMARTER_ORG_ID", org_id)
    with pytest.raises(errors.EngageSmarterError):
        client = Client()

    monkeypatch.setenv("ENGAGE_SMARTER_ORG_ID", org_id)
    monkeypatch.setenv("ENGAGE_SMARTER_API_KEY", api_key)
    client = Client()
    assert client is not None

    monkeypatch.setenv("ENGAGE_SMARTER_API_URL", custom_api_url + "/")
    client = Client()
    assert client._client.api_url == custom_api_url


def test_client_resources(mock_engagesmarter_client: Client) -> None:
    """Test Client resources."""
    client = mock_engagesmarter_client
    assert client is not None
    assert isinstance(client.agents, resources.AgentsResource)
    assert isinstance(client.conversations, resources.ConversationsResource)
    assert isinstance(client.runs, resources.RunsResource)
    assert isinstance(client.tags, resources.TagsResource)


def test_client_context_manager(mock_engagesmarter_client: Client) -> None:
    """Test Client context manager."""
    with mock_engagesmarter_client as client_cxt:
        assert client_cxt._client._client.is_closed is False
    assert client_cxt._client._client.is_closed
    assert mock_engagesmarter_client._client._client.is_closed


def test_authenticated_client_init(
    api_key: str,
    org_id: str,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test Authenticated Client."""
    monkeypatch.setenv("ENGAGE_SMARTER_API_KEY", api_key)
    monkeypatch.setenv("ENGAGE_SMARTER_ORG_ID", org_id)
    monkeypatch.delenv("ENGAGE_SMARTER_API_URL", raising=False)
    extra_headers = {"test": "test"}
    custom_timeout = 10

    # Override pointing to real API URL:
    client = Client()
    assert client._client is not None
    assert client._client.api_key == api_key
    assert client._client.org_id == org_id
    assert client._client.timeout == constants.DEFAULT_TIMEOUT
    assert client._client._headers == {}
    assert client._client.api_url == constants.DEFAULT_API_URL

    client = Client(
        extra_headers=extra_headers,
        timeout=custom_timeout,
    )
    assert client._client is not None
    assert client._client.timeout == custom_timeout
    assert client._client._headers == extra_headers
    assert client._client.get_headers() != extra_headers
    assert client._client.get_headers() == {
        constants.API_KEY_HEADER_NAME: api_key,
        constants.ORG_ID_HEADER_NAME: org_id,
        **extra_headers,
    }

    with Client()._client as client:
        assert client._client.is_closed is False
    assert client._client.is_closed
    with pytest.raises(RuntimeError):
        client.get("test")


def test_authenticated_client_http_methods(
    mock_engagesmarter_client: Client,
    mock_httpx_client: mock.Mock,
) -> None:
    """Test Authenticated Client HTTP methods."""
    auth_client = mock_engagesmarter_client._client
    with pytest.raises(httpx.ConnectError):
        auth_client.get("/ping")

    expected_data = {"response_key": "response_value"}
    expected_response = httpx.Response(status_code=200, json=expected_data)

    mock_httpx_client.get.return_value = expected_response
    mock_httpx_client.post.return_value = expected_response
    mock_httpx_client.patch.return_value = expected_response
    mock_httpx_client.delete.return_value = expected_response
    auth_client._client = mock_httpx_client

    assert auth_client.get("example_endpoint") == expected_data
    assert auth_client.delete("example_endpoint") == expected_data

    class MockContent(BaseModel):
        content_key: str

    content = MockContent(content_key="content_value")

    assert auth_client.post("example_endpoint", content=content) == expected_data
    assert (
        auth_client.post("example_endpoint", content=model_json(content))
        == expected_data
    )
    assert auth_client.patch("example_endpoint", content=content) == expected_data
    assert (
        auth_client.patch("example_endpoint", content=model_json(content))
        == expected_data
    )

    mock_httpx_client.get.assert_called_once_with("example_endpoint")
    mock_httpx_client.delete.assert_called_once_with("example_endpoint")
    mock_httpx_client.post.assert_called_with(
        "example_endpoint", content=model_json(content)
    )
    mock_httpx_client.post.call_count == 2
    mock_httpx_client.patch.assert_called_with(
        "example_endpoint", content=model_json(content)
    )
    mock_httpx_client.patch.call_count == 2
