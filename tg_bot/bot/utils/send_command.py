import logging
import shlex
import subprocess

import settings


async def _command(command_param: str):
    try:
        command_text = settings.__dict__[command_param]
    except Exception:
        raise ChildProcessError(f'Ошибка получения параметра {command_param if command_param else ''}')

    if not command_text or not command_text.strip():
        raise ChildProcessError(f'Не указан параметр {command_param if command_param else ''}')

    try:
        subprocess.run(shlex.split(command_text), encoding='utf-8')
        logging.info(f'Call command: {command_text}')
    except Exception:
        raise ChildProcessError(f'Ошибка выполнения команды [{command_text}]')


async def send_down():
    await _command('DOWN_COMMAND')


async def send_up():
    await _command('UP_COMMAND')
