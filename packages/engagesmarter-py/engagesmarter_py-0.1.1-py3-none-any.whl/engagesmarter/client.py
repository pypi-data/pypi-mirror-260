import os
import re
from typing import Dict

from ._auth_client import AuthenticatedClient
from .constants import DEFAULT_API_URL, DEFAULT_TIMEOUT
from .errors import EngageSmarterError
from .resources.agents import AgentsResource
from .resources.conversations import ConversationsResource
from .resources.runs import RunsResource
from .resources.tags import TagsResource


class Client:
    """
    The main synchronous Engage Smarter AI Platform client.
    """

    def __init__(
        self,
        *,
        api_url: str | None = None,
        api_key: str | None = None,
        org_id: str | None = None,
        timeout: int = DEFAULT_TIMEOUT,
        extra_headers: Dict[str, str] | None = None,
    ):
        """Construct a new synchronous client instance.

        This automatically infers the following arguments from their corresponding environment variables if they are not provided:
        - `api_key` from `ENGAGE_SMARTER_API_KEY`
        - `org_id` from `ENGAGE_SMARTER_ORG_ID`
        """

        api_url = api_url or os.getenv("ENGAGE_SMARTER_API_URL")
        api_url = api_url or DEFAULT_API_URL
        # Checking that the api_url does not end in '/'
        api_url = re.sub(r"\/$", "", api_url)

        api_key = api_key or os.getenv("ENGAGE_SMARTER_API_KEY")
        if api_key is None:
            raise EngageSmarterError(
                "api_key is required to use the Engage Smarter AI Platform API. Either pass it as an argument or set the ENGAGE_SMARTER_API_KEY environment variable."
            )

        org_id = org_id or os.getenv("ENGAGE_SMARTER_ORG_ID")
        if org_id is None:
            raise EngageSmarterError(
                "org_id is required to use the Engage Smarter AI Platform API. Either pass it as an argument or set the ENGAGE_SMARTER_ORG_ID environment variable."
            )

        headers = extra_headers or {}

        self._client = AuthenticatedClient(
            api_url=api_url,
            api_key=api_key,
            org_id=org_id,
            timeout=timeout,
            headers=headers,
        )

    def _check_engagesmarter_versions(self):
        """
        Check that the Engage Smarter API version is compatible with the SDK version.
        """
        # TODO: Discuss versioning
        raise NotImplementedError

    @property
    def agents(self):
        """
        The agents endpoint.
        """
        return AgentsResource(client=self._client)

    @property
    def conversations(self):
        """
        The conversations endpoint.
        """
        return ConversationsResource(client=self._client)

    @property
    def runs(self):
        """
        The runs endpoint.
        """
        return RunsResource(client=self._client)

    @property
    def tags(self):
        """
        The tags endpoint.
        """
        return TagsResource(client=self._client)

    def __del__(self):
        if hasattr(self, "_client"):
            del self._client

    # Context managers

    def close(self):
        self._client.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
