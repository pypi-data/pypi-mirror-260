from typing import Iterator

from ..constants import API_VERSION
from ..schemas.feedback import FeedbackRead, FeedbackUpsert
from ..schemas.messages import AgentMessage, MessageRead, UserMessage
from ..schemas.runs import RunRead
from .base import BaseResource


class RunsResource(BaseResource):
    _API_PREFIX: str = f"/{API_VERSION}/runs"

    def create_or_update_run_feedback(
        self, *, run_id: str, feedback: FeedbackUpsert
    ) -> FeedbackRead:
        """
        Creates or updates (upsert) run feedback.

        Feedback can comprise two fields: (1) a `thumbs` "up" or "down" rating, and (2) a free-text
        `comment`. If updating existing feedback by the user on a run, make sure to fill out whichever
        fields have previously been submitted, as otherwise the existing feedback will be overwritten.

        Args:
          run_id: The ID of the run to give feedback on.

          feedback: The user's feedback record to attach to the run.
        """
        response = self.client.post(
            f"{self._API_PREFIX}/{run_id}/feedback", content=feedback
        )
        return FeedbackRead(**response)

    def get_user_runs(
        self,
        *,
        tag_id: str | None = None,
        agent: str | None = None,
        reversed: bool = True,
        limit: int = 20,
        offset: int = 0,
    ) -> list[RunRead]:
        """
        Fetches a list of the user's run metadata records for the current organization.
        These records are created when a run is started, and contain information about
        the run, such as the agent used, the conversation ID, and the start time of the run.

        The list of runs will include runs which form part of conversations that the user
        has had via the API using an API key or in an app.

        Args:
          tag_id: Filter by tag ID.

          agent: Filter by agent.

          reversed: If True, get most recent run first. True by default.

          limit: The maximum number of runs to return.

          offset: The number of runs to skip before returning results.
        """
        query_params = {
            "reversed": reversed,
            "limit": limit,
            "offset": offset,
        }
        if tag_id is not None:
            query_params["tag_id"] = tag_id
        if agent is not None:
            query_params["agent"] = agent
        response = self.client.get(f"{self._API_PREFIX}/me", params=query_params)
        return [RunRead(**run) for run in response]

    def get_run_metadata(self, *, run_id: str) -> RunRead:
        """
        Fetches the metadata record for a single run. The run can be any within
        the user's current organization, not only the user's own runs.

        Args:
          run_id: The ID of the run to fetch.
        """
        response = self.client.get(f"{self._API_PREFIX}/{run_id}")
        return RunRead(**response)

    def get_run_messages(self, *, run_id: str) -> list[MessageRead]:
        """
        Fetches the messages for a single run. The run can be any within
        the user's current organization, not only the user's own runs.

        Args:
          run_id: The ID of the run to fetch.
        """
        response = self.client.get(f"{self._API_PREFIX}/{run_id}/messages")
        return [MessageRead(**message) for message in response]

    def get_run_feedback(self, *, run_id: str) -> list[FeedbackRead]:
        """
        Fetches the feedback for a single run. The run can be any within
        the user's current organization, not only the user's own runs.

        Args:
          run_id: The ID of the run to fetch.
        """
        response = self.client.get(f"{self._API_PREFIX}/{run_id}/feedback")
        return [FeedbackRead(**feedback) for feedback in response]

    def chat_with_agent(
        self,
        *,
        messages: list[AgentMessage | UserMessage | MessageRead],
        agent: str,
        stream: bool = False,
        return_inputs: bool = False,
        data: dict = {},
    ) -> list[MessageRead] | Iterator[MessageRead]:
        """
        Creates a new run by posting a history of user and agent messages, and expecting an agent message in response.
        The list of messages must be in ascending order, from oldest to most recent.

        A new conversation ID will be generated automatically for this run and will be returned on the agent message.
        The conversation can be continued using the conversations API by passing in the conversation ID found on
        messages returned by this method.

        If `stream=True` the response will be streamed as an event stream of status and agent messages.
        Messages can be accessed by iterating over the response.

        Args:
          messages: List of messages to send to the agent.

          agent: The name of the agent to use. The agent will respond to the latest message in the history.

          stream: If True, the response will be streamed as an event stream of status and agent messages.

          return_inputs: If True, returns the user inputs along with the agent response. This can be useful if you need
              access to the user message IDs for the conversation history.
        """
        query_params = {"agent": agent}
        messages = [message.model_dump() for message in messages]

        if return_inputs is True:
            query_params["return_inputs"] = return_inputs

        if stream is True:
            query_params["stream"] = stream
            iterator = self.client.post_stream(
                f"{self._API_PREFIX}/chat",
                params=query_params,
                content={"messages": messages, "data": data},
            )

            return (MessageRead(**message) for message in iterator)

        else:
            response = self.client.post(
                f"{self._API_PREFIX}/chat",
                params=query_params,
                content={"messages": messages, "data": data},
            )

            return [MessageRead(**message) for message in response]
