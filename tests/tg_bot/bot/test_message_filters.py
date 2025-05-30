from unittest.mock import MagicMock, patch

import pytest
from aiogram.enums import ChatType, ContentType
from aiogram.types import Message, CallbackQuery, Chat, User

import settings
from bot.message_filters import _get_message, filter_chat_type_private, filter_content_type_text, \
    filter_content_admin_user


def test__get_message():
    test_message_text = 'test_message_text'

    test_message = MagicMock(Message, return_value=test_message_text)
    assert _get_message(test_message).return_value == test_message_text

    test_message = MagicMock(CallbackQuery, message=test_message_text)
    assert _get_message(test_message) == test_message_text

    test_message = MagicMock(ContentType)
    assert _get_message(test_message) is None


@pytest.mark.asyncio
async def test_filter_chat_type_private():
    test_chat = MagicMock(Chat, type=ChatType.PRIVATE)
    test_message = MagicMock(Message, chat=test_chat)
    assert await filter_chat_type_private(test_message)

    test_chat = MagicMock(Chat, type=ChatType.GROUP)
    test_message = MagicMock(Message, chat=test_chat)
    assert not await filter_chat_type_private(test_message)


@pytest.mark.asyncio
async def test_filter_content_type_text():
    test_message = MagicMock(Message, content_type=ContentType.TEXT)
    assert await filter_content_type_text(test_message)

    test_message = MagicMock(Message, content_type=ContentType.AUDIO)
    assert not await filter_content_type_text(test_message)


@pytest.mark.asyncio
async def test_filter_content_admin_user():
    test_username = 'test_username'
    test_user = MagicMock(User, username=test_username)
    test_message = MagicMock(Message, from_user=test_user)

    with patch.dict(settings.__dict__, {'ADMINS': [test_username.upper()]}):
        assert await filter_content_admin_user(test_message)

    assert not await filter_content_admin_user(test_message)
