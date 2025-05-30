from unittest.mock import MagicMock

import pytest

from bot.utils.user import get_user_info


@pytest.mark.parametrize(['id', 'username', 'first_name', 'last_name'], (
        ('1', 'test_user_name', 'test_first_name', 'test_last_name'),
        ('2', 'test_user_name', 'test_first_name', ''),
        ('3', 'test_user_name', '', ''),
        ('', '', '', '')))
@pytest.mark.asyncio
async def test_get_user_info(id, username, first_name, last_name):
    from_test_user = MagicMock(id=id, username=username, first_name=first_name, last_name=last_name)
    test_message = MagicMock(from_user=from_test_user)

    test_result = await get_user_info(test_message)
    assert test_result['id'] == id if id else '0'
    assert test_result['username'] == username if username else '-'
    assert test_result['name'] == ' '.join((first_name if first_name else '-', last_name if last_name else '-')).strip()
