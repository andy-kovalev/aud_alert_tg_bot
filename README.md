# aud_alert_tg_bot
Telegram bot providing alert message

# Установка сервиса

## Install Python
Проверить версию Python
```shell
python3 --version
```
Установить Python, версии 3.10 и выше, желательна последняя версия https://www.python.org/downloads/
```shell
apt update
apt install python3.13.3
```
Установить пакетный менеджер pip
```shell
apt install python3-pip
```
или обновить установленный
```shell
python3.13.3 -m pip install --upgrade pip
```
Установить пакет для создания виртуального окружения venv
```shell
apt install python3-venv
```
или обновить установленный
```shell
python3.13.3 -m pip install --upgrade venv
```
Создать виртуальное окружение venv в каталоге venv_path
```shell
python3.13.3 -m venv venv_path
```
Активировать виртуальное окружение python в каталоге venv_path
```shell
source ./venv/bin/activate
```


## Install dependencies
При использовании виртуального окружения python, перед выполнением команд необходимо активировать виртуальное окружение
<br><br>
Установить зависимости библиотек
```shell
pip install -r requirements.txt
```

## Настройки для работы 
Перед запуском, необходимо задать параметры в конфигурационном фале формата .env
<br><br>
По умолчанию используется файл с именем ***.env***
<br>
Файл .env может иметь любое имя, чтобы скрипт настройки использовал файл
необходимо имя файла передать в исполняемый скрипт, указав значение в переменной окружения *ENV_FILENAME*
```shell
export ENV_FILENAME="./settings.env"
```
Пример заполнения файла настроек:
```dotenv
# logging param
# Имя файла для записи логов
LOG_FILE_NAME=./tests/logs/aud_alert_tg_bot.log
# Уровень записи логов CRITICAL, ERROR, WARNING, INFO, DEBUG
LOG_LEVEL=DEBUG

# bot param
# Токен Telegram бота
BOT_TOKEN=./.key/aud_alert_tg_bot.key

# admin param
# Список имен пользователей Telegram (UserName), которые обладают администраторскими правами
# эти пользователи имеют возможность запускать UP команду
ADMINS=@Admin_User_tgName

# command param
# команды запуска Shell скриптов
# Команда выключения
DOWN_COMMAND="./command/down.sh param1 param2"
# Команда включения
UP_COMMAND=./command/up.sh
```

# Использование сервиса
Задать параметры в конфигурационном фале
Указать путь к конфигурационному файлу в переменной окружения *ENV_FILENAME*
Запустить на исполнение скрипт
```shell
python3.13.3 ./tg_bot/__main__.py
```
или использовать подготовленный bash скрипт
```shell
bash run_app.sh
```

## Автозапуск севиса после перезагрузки OS
Добавить в *crontab*
```shell
crontab -e #[вставить текст]
@reboot /path_to_service/aud_alert_tg_bot/run_app.sh.sh
#[вставить текст]
```
```shell
nano /etc/systemd/system/aud_alert.service #[вставить текст]
ini
[Unit]
Description=Up aud_alert_tg_bot service
[Service]
ExecStart=/path_to_service/aud_alert_tg_bot/run_app.sh.sh
Type=simple
Restart=on-failure
[Install]
WantedBy=multi-user.target
#[вставить текст]
```

## Прочие настройки OS

* настроить мониторинг работы сервиса, предлагаю через поиск слова CRITICAL в лог файле
* настроить очистку/архивирование лог файла, чтобы не заполнить им пространство OS

