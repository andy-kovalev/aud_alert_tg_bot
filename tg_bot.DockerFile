FROM python:3.13.1
RUN apt update; apt install netcat-traditional

RUN python3 -m pip install pip --upgrade

RUN mkdir -p /usr/src_run_config/
WORKDIR /usr/src_run_config/

COPY ./.env/docker.env ./.env
ENV ENV_FILENAME=/usr/src_run_config/.env

COPY ./.key/aud_alert_tg_bot.key ./.key
ENV BOT_TOKEN=/usr/src_run_config/.key

COPY ./requirements.txt ./requirements.txt
RUN pip3 install --no-cache-dir --upgrade -r ./requirements.txt

RUN mkdir -p /usr/src_run_command
WORKDIR /usr/src_run_command/
COPY ./command/up.sh ./up.sh
COPY ./command/down.sh ./down.sh


WORKDIR /usr/src/
COPY ./tg_bot ./

CMD python3 __main__.py
