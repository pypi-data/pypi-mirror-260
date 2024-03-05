from client.engagesmarter import Client
from client.engagesmarter.resources.base import BaseResource


def test_base_resource_init(mock_engagesmarter_client: Client) -> None:
    auth_client = mock_engagesmarter_client._client
    base_resource = BaseResource(client=auth_client)
    assert base_resource.client == auth_client
