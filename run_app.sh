#!/bin/bash
export ENV_FILENAME="./.env/settings.env"
source ./venv/bin/activate
python3 ./tg_bot/__main__.py
