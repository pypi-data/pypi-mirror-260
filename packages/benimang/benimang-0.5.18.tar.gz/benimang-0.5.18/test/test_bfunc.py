import pytest

from beni.bfunc import deobfuscate, obfuscate

_DATA = '(故意地)混淆，使困惑，使模糊不清to make sth less clear and more difficult to understand, usually deliberately'.encode()


@pytest.mark.asyncio
async def test_obfuscate():
    magicContent = obfuscate(_DATA)
    assert deobfuscate(magicContent) == _DATA
