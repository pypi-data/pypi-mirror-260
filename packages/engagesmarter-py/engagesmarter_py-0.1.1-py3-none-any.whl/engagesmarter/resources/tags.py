from ..constants import API_VERSION
from ..schemas.base import Success
from ..schemas.conversations import ConversationRead
from ..schemas.runs import RunRead
from ..schemas.tags import TagCreate, TagRead, TagUpdate
from .base import BaseResource


class TagsResource(BaseResource):
    _API_PREFIX: str = f"/{API_VERSION}/tags"

    def search(
        self, *, search: str = "", limit: int = 20, offset: int = 0
    ) -> list[TagRead]:
        """
        Searches for tags with names or descriptions matching the given search string.
        Only searches for tags available within the current organization.

        Args:
          search: A search string to search for among tag names and descriptions.

          limit: The maximum number of tags to return.

          offset: The number of tags to skip before returning results.
        """
        response = self.client.get(
            f"{self._API_PREFIX}",
            params={"search": search, "limit": limit, "offset": offset},
        )
        return [TagRead(**tag_dict) for tag_dict in response]

    def create(self, *, name: str, description: str = "") -> TagRead:
        """
        Creates a new tag in the current organization.

        Args:
          name: The name of the tag.

          description: A description of the tag. If not provided, defaults to an empty string.
        """
        content = TagCreate(name=name, description=description)
        response = self.client.post(f"{self._API_PREFIX}", content=content)
        return TagRead(**response)

    def get_tag(self, *, tag_id: str) -> TagRead:
        """
        Fetches a single tag by ID from within the current organization.

        Args:
          tag_id: The ID of the tag to fetch.
        """
        response = self.client.get(f"{self._API_PREFIX}/{tag_id}")
        return TagRead(**response)

    def update_tag(self, *, tag_id: str, description: str | None = None) -> TagRead:
        """
        Updates a single tag by ID from within the current organization.

        Args:
          tag_id: The ID of the tag to update.

          description: A description of the tag.
        """
        content = TagUpdate(description=description)
        response = self.client.patch(f"{self._API_PREFIX}/{tag_id}", content=content)
        return TagRead(**response)

    def delete_tag(self, *, tag_id: str) -> Success:
        """
        Deletes a single tag by ID from within the current organization.

        Args:
          tag_id: The ID of the tag to delete.
        """
        response = self.client.delete(f"{self._API_PREFIX}/{tag_id}")
        return Success(**response)

    def get_tagged_conversations(
        self, *, tag_id: str, limit: int = 20, offset: int = 0
    ) -> list[ConversationRead]:
        """
        Fetches a list of metadata objects for conversations that have been linked to a given tag.

        Args:
          tag_id: The ID of the tag to fetch conversations for.

          limit: The maximum number of conversations to return.

          offset: The number of conversations to skip before returning results.
        """
        response = self.client.get(
            f"{self._API_PREFIX}/{tag_id}/conversations",
            params={"limit": limit, "offset": offset},
        )
        return [ConversationRead(**conversation) for conversation in response]

    def get_tagged_runs(
        self, *, tag_id: str, limit: int = 20, offset: int = 0
    ) -> list[RunRead]:
        """
        Fetches a list of metadata objects for runs that have been linked to a given tag.

        Args:
          tag_id: The ID of the tag to fetch runs for.

          limit: The maximum number of runs to return.

          offset: The number of runs to skip before returning results.
        """
        response = self.client.get(
            f"{self._API_PREFIX}/{tag_id}/runs",
            params={"limit": limit, "offset": offset},
        )
        return [RunRead(**run) for run in response]
