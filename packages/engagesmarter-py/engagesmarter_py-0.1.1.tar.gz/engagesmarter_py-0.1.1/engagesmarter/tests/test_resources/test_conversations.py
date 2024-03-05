from datetime import datetime

import pytest

from client.engagesmarter import Client
from client.engagesmarter.resources.conversations import ConversationsResource
from client.engagesmarter.schemas.conversations import (
    ConversationCreate,
    ConversationRead,
    ConversationUpdate,
)
from client.engagesmarter.schemas.messages import MessageRead, UserMessage


def test_conversations_init(
    mock_engagesmarter_client: Client,
) -> None:
    conversations = mock_engagesmarter_client.conversations
    assert conversations is not None
    assert conversations.client == mock_engagesmarter_client._client
    assert conversations._API_PREFIX == "/v1/conversations"


# @pytest.mark.slow
# @pytest.mark.parametrize("data", [None, {}, {"foo": "bar"}])
# def test_conversations_create(
#     conversations: ConversationsResource,
#     data: dict | None,
# ) -> None:
#     if data is not None:
#         conversation_create = ConversationCreate(data=data)
#         conversation_read = conversations.create(
#             conversation=conversation_create,
#         )
#         assert conversation_read.data == data
#     else:
#         conversation_read = conversations.create()
#         assert conversation_read.data == {}
#     assert conversation_read is not None
#     assert isinstance(conversation_read, ConversationRead)
#     assert isinstance(conversation_read.id, str)
#     assert isinstance(conversation_read.created, datetime)
#     assert conversation_read.org_id == conversations.client.org_id
#     assert conversation_read.cloned_from_message_id is None


# @pytest.mark.slow
# def test_conversations_chat_with_agent(
#     conversations: ConversationsResource,
# ) -> None:
#     conversation_id = conversations.create().id
#     user_message = UserMessage(content="Hi, what can you help me with?")
#     agent = "parrot"

#     # No streaming
#     agent_message = conversations.chat_with_agent(
#         conversation_id=conversation_id,
#         user_message=user_message,
#         agent=agent,
#     )
#     assert agent_message is not None
#     assert isinstance(agent_message, MessageRead)
#     assert agent_message.conversation_id == conversation_id
#     assert isinstance(agent_message.id, str)
#     assert agent_message.org_id == conversations.client.org_id
#     assert isinstance(agent_message.run_id, str)
#     assert isinstance(agent_message.created, datetime)
#     assert agent_message.role == "agent"
#     assert agent_message.name == agent
#     assert isinstance(agent_message.user_id, str)
#     assert agent_message.content == f"You said: {user_message.content}"

#     # Streaming
#     stream_messages = conversations.chat_with_agent(
#         conversation_id=conversation_id,
#         user_message=user_message,
#         agent=agent,
#         stream=True,
#     )
#     assert stream_messages is not None
#     assert isinstance(stream_messages, list)
#     assert len(stream_messages) >= 1
#     assert isinstance(stream_messages[0], MessageRead | MessageCreate)


# @pytest.mark.slow
# @pytest.mark.parametrize("data", [None, {}, {"foo": "bar"}])
# def test_conversations_clone_conversation(
#     conversations: ConversationsResource,
#     data: dict | None,
# ) -> None:
#     conversation_id = conversations.create().id
#     user_message = UserMessage(content="Hi, what can you help me with?")
#     agent = "parrot"
#     agent_message = conversations.chat_with_agent(
#         conversation_id=conversation_id,
#         user_message=user_message,
#         agent=agent,
#         stream=False,
#     )
#     message_id = agent_message.id
#     if data is not None:
#         cloned_conversation = conversations.clone_conversation(
#             message_id=message_id,
#             conversation=ConversationUpdate(data=data),
#         )
#         assert cloned_conversation.data == data
#     else:
#         cloned_conversation = conversations.clone_conversation(
#             message_id=message_id,
#         )
#         assert cloned_conversation.data == {}
#     assert cloned_conversation is not None
#     assert isinstance(cloned_conversation, ConversationRead)
#     assert cloned_conversation.id != conversation_id
#     assert cloned_conversation.org_id == conversations.client.org_id
#     assert cloned_conversation.cloned_from_message_id == message_id
