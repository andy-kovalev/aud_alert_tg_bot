from aiogram.enums import ChatType, ContentType
from aiogram.types import Message, CallbackQuery

import settings


# lambda msg: msg.chat.type == ChatType.PRIVATE
def _get_message(message):
    if isinstance(message, Message):
        return message
    elif isinstance(message, CallbackQuery):
        return message.message
    else:
        return None


async def filter_chat_type_private(message) -> bool:
    msg: Message = _get_message(message)
    if msg:
        return msg.chat.type == ChatType.PRIVATE
    else:
        return False


async def filter_content_type_text(message) -> bool:
    msg: Message = _get_message(message)
    if msg:
        return msg.content_type == ContentType.TEXT
    else:
        return False


async def filter_content_admin_user(message) -> bool:
    msg: Message = _get_message(message)
    if msg:
        return msg.from_user.username.upper() in settings.ADMINS
    else:
        return False
