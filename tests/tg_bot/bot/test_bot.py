from importlib import reload
from unittest.mock import patch, MagicMock


def test_bot_dispatcher():
    with patch('aiogram.Dispatcher', return_value=MagicMock()):
        from bot import bot
        reload(bot)
        test_dispatcher = bot.dp
        assert isinstance(test_dispatcher, MagicMock)


def test_bot_dispatcher_exception():
    with patch('aiogram.Dispatcher', new=Exception()):
        from bot import bot
        reload(bot)
        test_dispatcher = bot.dp
        assert test_dispatcher is None


def test_bot_bot_exception():
    with patch('aiogram.Bot', new=Exception()):
        from bot import bot
        reload(bot)
        test_bot = bot.bot
        assert test_bot is None
