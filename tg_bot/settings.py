"""
Настройки для работы

Пользовательская настройка производится в файле конфигурации в формате .env

Файл .env может иметь любое имя, чтобы скрипт настройки использовал файл
необходимо
  - либо указать значение в переменной окружения ENV_FILENAME
  - либо указать этот файл в параметре командной строки --envfile {файл}

По умолчанию используется файл .env
"""

import logging
from datetime import datetime
from os import path, getenv, environ

from dotenv import load_dotenv


def configure_logging(log_file_name, log_level, log_format):
    """
    Настройка логирования
    """
    # default logging
    handlers = []
    if log_file_name:
        file_log = logging.FileHandler(log_file_name, encoding='utf-8')
        handlers.append(file_log)
    console_out = logging.StreamHandler()
    handlers.append(console_out)

    logging.basicConfig(handlers=handlers, level=log_level, format=log_format)


def get_env_param(name: str, required: bool = False, default=None, log_text=None):
    result = getenv(name, default=default if default else '')
    if required and not result:
        exit('%s %s: root: settings: %s не задан' % (
            datetime.now().isoformat(sep=' ', timespec='milliseconds'), logging.getLevelName(logging.CRITICAL), name))
    else:
        logging.debug('settings: %s=%s', name, log_text if log_text else result)
    return result


def get_int_env_param(name: str, required: bool = False, default=None, log_text=None) -> int | str:
    result = get_env_param(name, required, default, log_text)
    if result.isdigit():
        result = int(result)
    else:
        logging.error('settings: %s=%s, не является числом', name, log_text if log_text else result)
    return result


def get_obfuscate_env_param_value(value):
    def fill_asterisk(fill_count):
        return '*' * fill_count

    if not value or len(value) == 0:
        return ''
    elif len(value) > 3:
        inx = 1 if len(value) < 9 else 3
        return value[:inx] + fill_asterisk(len(value) - inx * 2) + value[-inx:]
    elif len(value) > 0:
        return fill_asterisk(len(value))


def get_connect_uri(protocol, resource, address, port=None, user=None, password=None) -> str:
    """
    Формирует URL для подключения к сервисам
    :param protocol: протокол подключения (redis, mongodb, http)
    :param resource: ресурс подключения (db_number, db_name, endpoint)
    :param address: адрес
    :param port: порт
    :param user: имя пользователя
    :param password: пароль пользователя
    :return: URI подключения к в формате protocol://[user:password@]address[:port]/resource
    """
    user_str = f'{user}{f":{password}" if password else ""}@' if user else ''
    port_str = f':{port}' if port else ''

    return '%s://%s%s%s/%s' % (protocol, user_str, address, port_str, resource) if address else ''


def set_bot_token_from_file(param):
    def get_text_from_file(file_name):
        with open(file_name, 'r') as text_file:
            text = text_file.read()
        return text.strip()

    param_value = path.abspath(getenv(param))
    if path.exists(param_value) and path.isfile(param_value):
        environ[param] = get_text_from_file(param_value)


# .env файл для загрузки параметров
ENV_FILENAME = path.abspath(getenv('ENV_FILENAME', default='.env'))
if path.exists(ENV_FILENAME) and path.isfile(ENV_FILENAME):
    load_dotenv(ENV_FILENAME)

# logging param
# Имя файла для записи логов
LOG_FILE_NAME = path.abspath(getenv('LOG_FILE_NAME', default='aud_alert_tg_bot.log'))

# Уровень записи логов ERROR, WARNING, DEBUG, INFO
LOG_LEVEL = logging.getLevelName(getenv('LOG_LEVEL', default='INFO'))
LOG_FORMAT = getenv('LOG_FORMAT', default='%(asctime)s %(levelname)s: %(name)s: %(message)s')

configure_logging(LOG_FILE_NAME, LOG_LEVEL, LOG_FORMAT)

logging.debug('settings: ENV_FILENAME=%s', ENV_FILENAME)
logging.debug('settings: LOG_FILE_NAME=%s', LOG_FILE_NAME)
logging.debug('settings: LOG_LEVEL=%s', logging.getLevelName(LOG_LEVEL))
logging.debug('%s', '-' * 20)

# bot param
# Токен Telegram бота
set_bot_token_from_file('BOT_TOKEN')
BOT_TOKEN_OBFUSCATED = get_obfuscate_env_param_value(getenv('BOT_TOKEN'))
BOT_TOKEN = get_env_param('BOT_TOKEN', required=True, log_text=BOT_TOKEN_OBFUSCATED)

logging.debug('%s', '-' * 20)

# admin param
# Список имен пользователей Telegram (UserName), которые оладают администраторскими правами
# эти пользователи имеют возможность запускать UP команду
ADMINS = get_env_param('ADMINS')
ADMINS = ADMINS.replace('@', '').upper().split(',')

# command param
# команды запуска Shell скриптов
# Команда выключения
DOWN_COMMAND = get_env_param('DOWN_COMMAND')

# Команда включения
UP_COMMAND = get_env_param('UP_COMMAND')
