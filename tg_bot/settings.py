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
from os import path, getenv

from env_settings import configure, load_env_params
from env_settings import get_str_env_param, get_values
from env_settings.utils import _get_obfuscate_value as get_obfuscate_value

configure(error_handling='exit', do_value_logging=True)


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


# .env файл для загрузки параметров
ENV_FILENAME = path.abspath(getenv('ENV_FILENAME', default='.env'))
if path.exists(ENV_FILENAME) and path.isfile(ENV_FILENAME):
    load_env_params(ENV_FILENAME)

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
BOT_TOKEN = get_values(get_str_env_param('BOT_TOKEN', required=True, do_obfuscate_log_text=True))[0]
BOT_TOKEN_OBFUSCATED = get_obfuscate_value('BOT_TOKEN')

logging.debug('%s', '-' * 20)

# admin param
# Список имен пользователей Telegram (UserName), которые оладают администраторскими правами
# эти пользователи имеют возможность запускать UP команду
ADMINS = get_str_env_param('ADMINS')
ADMINS = ADMINS.replace('@', '').upper().split(',') if ADMINS else []

# command param
# команды запуска Shell скриптов
# Команда выключения
DOWN_COMMAND = get_str_env_param('DOWN_COMMAND')

# Команда включения
UP_COMMAND = get_str_env_param('UP_COMMAND')
