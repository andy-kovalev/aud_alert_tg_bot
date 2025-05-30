import logging

from aiogram import types, Dispatcher
from aiogram.fsm.context import FSMContext

from bot.const.const_message import SUCCESS_ALERT_TEXT, FAULT_ALERT_TEXT
from bot.message_filters import filter_chat_type_private, filter_content_type_text, filter_content_admin_user
from bot.utils.send_command import send_down, send_up
from bot.utils.user import get_user_info


def logging_critical(command: str, err):
    logging.critical(f'alert: Can\'t send {command}! [{err}]')


async def txt_command(message: types.Message, state: FSMContext):
    if await filter_content_admin_user(message) and message.text.upper() in (
            'UP', 'BOOT', 'REBOOT', 'ПОДНЯТЬ', 'ЗАПУСК', 'ЗАПУСТИТЬ', 'ЗАГРУЗКА', 'ЗАГРУЗИТЬ'):
        try:
            await send_up()
            await message.answer(SUCCESS_ALERT_TEXT)
        except Exception as err:
            logging_critical('up', err)
            await message.answer(FAULT_ALERT_TEXT)
    else:
        user_info = await get_user_info(message)
        logging.debug('Chat[%s], Text[%s], User[%s]', message.chat.id, message.text,
                      ';'.join((user_info['id'], user_info['username'], user_info['name'])))

        try:
            await send_down()
            await message.answer(SUCCESS_ALERT_TEXT)
        except Exception as err:
            logging_critical('down', err)
            await message.answer(FAULT_ALERT_TEXT)


def register_handlers(dp: Dispatcher):
    dp.message.register(txt_command, filter_chat_type_private, filter_content_type_text)
