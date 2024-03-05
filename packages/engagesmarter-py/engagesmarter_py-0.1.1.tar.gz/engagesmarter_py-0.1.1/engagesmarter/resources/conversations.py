from __future__ import annotations

from typing import Iterator

from ..constants import API_VERSION
from ..schemas.conversations import (
    ConversationCreate,
    ConversationRead,
    ConversationUpdate,
)
from ..schemas.feedback import FeedbackRead
from ..schemas.messages import AgentMessage, MessageRead, UserMessage
from ..schemas.runs import RunRead
from ..schemas.tags import TagRead
from .base import BaseResource


class ConversationsResource(BaseResource):
    _API_PREFIX: str = f"/{API_VERSION}/conversations"

    def create(
        self, *, conversation: ConversationCreate | None = None
    ) -> ConversationRead:
        """
        Creates a new conversation and get new conversation read object,
        including the conversation_id.

        Args:
          conversation: If specified, any data included in the `data` field will be included as
              metadata within the conversation. We recommend structuring this metadata as a JSON
              encodable dictionary.

              This can be useful for including additional context about the conversation.
        """
        if conversation is None:
            conversation = ConversationCreate()
        response = self.client.post(self._API_PREFIX, content=conversation)
        return ConversationRead(**response)

    def clone_conversation(
        self,
        *,
        message_id: str,
        conversation: ConversationUpdate | None = None,
    ) -> ConversationRead:
        """
        Clones a new conversation from a full or partial existing conversation. This works by
        cloning an existing conversation up to and including the agent message with the specified
        `message_id`. The new conversation will have a new `conversation_id`, which is different
        from the existing one.

        Args:
          message_id: The ID of the agent message up to which to clone an existing conversation.
              The system uses the agent message ID to identify a particular run step in the
              conversation.

          conversation: If specified, any data included in the `data` field will be included as
              metadata within the conversation. We recommend structuring this metadata as a JSON
              encodable dictionary.

              This can be useful for including additional context about the conversation.
        """
        if conversation is None:
            conversation = ConversationUpdate()
        query_params = {"message_id": message_id}
        response = self.client.post(
            f"{self._API_PREFIX}/clone",
            content=conversation,
            params=query_params,
        )
        return ConversationRead(**response)

    def search_own_conversations(
        self,
        *,
        tag_id: str | None = None,
        reversed: bool = True,
        limit: int = 20,
        offset: int = 0,
    ) -> list[ConversationRead]:
        """
        Fetches metadata on user's past conversations within the organization.
        If a user's API key is shared by multiple end users, then it will return conversations
        across all those end users.

        By default, it returns the most recent conversations first. It can additionally be
        filtered by `tag_id`.

        Args:
          tag_id: If specified, only conversations with the specified tag will be returned.

          reversed: If True, returns the most recent conversations first. Otherwise, returns the
              oldest conversations first.

          limit: Number of conversations to return.

          offset: Number of conversations to skip.
        """
        query_params = {
            "reversed": reversed,
            "limit": limit,
            "offset": offset,
        }
        if tag_id:
            query_params["tag_id"] = tag_id
        response = self.client.get(f"{self._API_PREFIX}/me", params=query_params)
        return [ConversationRead(**conversation_dict) for conversation_dict in response]

    def search_saved_conversations(
        self, *, reversed: bool = True, limit: int = 20, offset: int = 0
    ) -> list[ConversationRead]:
        """
        Fetches metadata on user's saved conversations within the organization. Saved conversations
        can be any conversations carried out within the organization, not only the user's own.

        By default, it returns the most recent conversations first.

        Args:
          reversed: If True, returns the most recent conversations first. Otherwise, returns the
              oldest conversations first.

          limit: Number of conversations to return.

          offset: Number of conversations to skip.
        """
        query_params = {
            "reversed": reversed,
            "limit": limit,
            "offset": offset,
        }
        response = self.client.get(f"{self._API_PREFIX}/saved", params=query_params)
        return [ConversationRead(**conversation_dict) for conversation_dict in response]

    def get_conversation_metadata(self, *, conversation_id: str) -> ConversationRead:
        """
        Fetches metadata on a specified conversation.

        Args:
          conversation_id: The ID of the conversation for which to get the metadata.
        """
        response = self.client.get(f"{self._API_PREFIX}/{conversation_id}")
        return ConversationRead(**response)

    def update_conversation_metadata(
        self, *, conversation_id: str, conversation: ConversationUpdate
    ) -> ConversationRead:
        """
        Updates metadata on a specified conversation.

        Args:
          conversation_id: The ID of the conversation for which to update the metadata.

          conversation: The updated conversation metadata.
        """
        response = self.client.patch(
            f"{self._API_PREFIX}/{conversation_id}",
            content=conversation,
        )
        return ConversationRead(**response)

    def save_conversation(self, *, conversation_id: str) -> ConversationRead:
        """
        Adds a specified conversation to user's saved conversations list. The conversation can
        be any conversation carried out within the organization, not only the user's own. The
        user is identified based on the API key being used.

        Args:
          conversation_id: The ID of the conversation to save.
        """
        response = self.client.post(f"{self._API_PREFIX}/{conversation_id}/saved")
        return ConversationRead(**response)

    def unsave_conversation(self, *, conversation_id: str) -> ConversationRead:
        """
        Removes a specified conversation from user's saved conversations list.
        This does not delete the underlying conversation and only removes a reference
        to it in the user's list. The user is identified based on the API key being used.

        Args:
          conversation_id: The ID of the conversation to remove.
        """
        response = self.client.delete(f"{self._API_PREFIX}/{conversation_id}/saved")
        return ConversationRead(**response)

    def add_messages_to_conversation_history(
        self, *, messages: list[UserMessage | AgentMessage]
    ) -> list[MessageRead]:
        """
        Adds messages to a specified conversation's message history without triggering an agent
        response. Messages are added in the order in which they are provided.
        """
        response = self.client.post(
            f"{self._API_PREFIX}/messages",
            content=[message.model_dump() for message in messages],
        )
        return [MessageRead(**message_dict) for message_dict in response]

    def get_conversation_message_history(
        self, *, conversation_id: str
    ) -> list[MessageRead]:
        """
        Fetches the full message history for a specified conversation.

        Args:
          conversation_id: The ID of the conversation for which to get the message history.
        """
        response = self.client.get(f"{self._API_PREFIX}/{conversation_id}/messages")
        return [MessageRead(**message_dict) for message_dict in response]

    def get_conversation_feedback(self, *, conversation_id: str) -> list[FeedbackRead]:
        """
        Fetches all feedback submitted for a specified conversation.

        Args:
          conversation_id: The ID of the conversation for which to get the feedback.
        """
        response = self.client.get(f"{self._API_PREFIX}/{conversation_id}/feedback")
        return [FeedbackRead(**feedback_dict) for feedback_dict in response]

    def get_conversation_runs(self, *, conversation_id: str) -> list[RunRead]:
        """
        Fetches the information on individual runs within a specified conversation. Each run
        represent a particular step in the conversation - one interaction between a user and
        the agent.

        Args:
          conversation_id: The ID of the conversation for which to get the runs.
        """
        response = self.client.get(f"{self._API_PREFIX}/{conversation_id}/runs")
        return [RunRead(**run_dict) for run_dict in response]

    def get_conversation_tags(self, *, conversation_id: str) -> list[TagRead]:
        """
        Fetches all tags associated with a specified conversation.

        Args:
          conversation_id: The ID of the conversation for which to get the tags.
        """
        response = self.client.get(f"{self._API_PREFIX}/{conversation_id}/tags")
        return [TagRead(**tag_dict) for tag_dict in response]

    def add_tag_to_conversation(
        self, *, conversation_id: str, tag_id: str
    ) -> list[TagRead]:
        """
        Adds a tag to a specified conversation. Returns all tags associated with the conversation.

        Args:
          conversation_id: The ID of the conversation to tag.

          tag_id: The ID of the tag to add.
        """
        response = self.client.post(
            f"{self._API_PREFIX}/{conversation_id}/tags/{tag_id}"
        )
        return [TagRead(**tag_dict) for tag_dict in response]

    def remove_tag_from_conversation(
        self, *, conversation_id: str, tag_id: str
    ) -> list[TagRead]:
        """
        Removes a tag from a specified conversation. Returns all tags associated with the
        conversation.

        Args:
          conversation_id: The ID of the conversation to untag.

          tag_id: The ID of the tag to remove.
        """
        response = self.client.delete(
            f"{self._API_PREFIX}/{conversation_id}/tags/{tag_id}"
        )
        return [TagRead(**tag_dict) for tag_dict in response]

    def chat_with_agent(
        self,
        *,
        conversation_id: str,
        messages: list[UserMessage],
        agent: str,
        stream: bool = False,
        return_inputs: bool = False,
    ) -> list[MessageRead] | Iterator[MessageRead]:
        """
        Posts new message(s) to the agent on this conversation and gets a list of messages as a response.
        For most use cases, the new message will be a single user message. Messages sent with the request
        will be saved to the conversation history and then used by the agent.

        If sending more than one message, the list of messages must be in ascending order, from oldest to most
        recent. Be careful not to include any messages multiple times otherwise the agent will see multiple copies of
        messages and may be confused.

        If called with an empty message list in the request `[]` then the agent will be called with no messages.
        The agent will only respond if the message most recently saved to the conversation history was a user message.

        If `stream=True` the response will be streamed as an event stream of status and agent messages.
        Messages can be accessed by iterating over the response.

        Args:
          conversation_id: The ID of the conversation to post messages to.

          messages: List of messages to send to the agent.

          agent: The name of the agent to send the message to.

          stream: If True, the response will be streamed as an event stream of status and agent messages.

          return_inputs: If True, returns the user inputs along with the agent response. This can be useful if you need
              access to the user message IDs for the
               conversation history.
        """
        query_params = {"agent": agent}
        messages = [message.model_dump() for message in messages]

        if return_inputs is True:
            query_params["return_inputs"] = return_inputs

        if stream is True:
            query_params["stream"] = stream
            iterator = self.client.post_stream(
                f"{self._API_PREFIX}/{conversation_id}/chat",
                params=query_params,
                content={"messages": messages},
            )

            return (MessageRead(**message) for message in iterator)

        else:
            response = self.client.post(
                f"{self._API_PREFIX}/{conversation_id}/chat",
                params=query_params,
                content={"messages": messages},
            )

            return [MessageRead(**message) for message in response]
