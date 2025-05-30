from types import MethodType, FunctionType, ModuleType

import pytest

from bot.const import const_message


def test_const_message():
    const_param = [v for v in vars(const_message) if not isinstance(getattr(const_message, v), (
        type, MethodType, FunctionType, ModuleType)) and not v.startswith('__')]

    consts = ('HELP_TEXT', 'START_TEXT', 'SUCCESS_ALERT_TEXT', 'FAULT_ALERT_TEXT')

    for param in const_param:
        if param not in consts:
            pytest.fail(f'Константа {param} добавлена в const_message.py и не указан в тесте')

    for const in consts:
        if const not in const_param:
            pytest.fail(f'Константа {const} указана в тесте и не добавлена в const_message.py')
