from unittest.mock import patch

import pytest

from bot.utils.send_command import send_down, send_up, _command


@pytest.mark.asyncio
async def test_command(monkeypatch):
    param_name = 'DOWN_COMMAND'
    test_param_value = 'test_param_value'

    with patch('.'.join(['settings', param_name]), return_value=test_param_value):
        with patch('shlex.split', return_value=test_param_value):
            with patch('subprocess.run') as mocked_run:
                await _command(param_name)
                mocked_run.assert_called_once_with(test_param_value, encoding='utf-8')

    with pytest.raises(ChildProcessError) as exc_info:
        with patch('.'.join(['settings', param_name]), return_value=test_param_value):
            with patch('shlex.split', return_value=test_param_value):
                await _command(param_name)
    assert 'Ошибка выполнения команды' in str(exc_info.value)

    with pytest.raises(ChildProcessError) as exc_info:
        with patch('.'.join(['settings', param_name]), return_value=''):
            with patch('.'.join(['settings', param_name, 'strip']), return_value=''):
                await _command(param_name)
    assert 'Не указан параметр' in str(exc_info.value)

    with pytest.raises(ChildProcessError) as exc_info:
        await _command('TEST_PARAM')
    assert 'Ошибка получения параметра' in str(exc_info.value)


@pytest.mark.asyncio
async def test_send_down():
    with patch('bot.utils.send_command._command') as mocked_command:
        await send_down()
        mocked_command.assert_called_once_with('DOWN_COMMAND')


@pytest.mark.asyncio
async def test_send_up():
    with patch('bot.utils.send_command._command') as mocked_command:
        await send_up()
        mocked_command.assert_called_once_with('UP_COMMAND')
