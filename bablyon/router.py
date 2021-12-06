import re
import typing as t

from bablyon.utils import format_pattern
from asyncio import iscoroutinefunction


class Router:
    def __init__(
        self,
        url:str,
        func:t.Awaitable,
        is_static:bool=False
    ) -> None:
        self.url = url
        self.pattren = format_pattern(url)
        self.func = func
        self.is_static = is_static

    async def __call__(self,*args):
        return await self.func(*args)

class HTTPErrorRouter:
    def __init__(
        self,
        status_code:str,
        func:t.Awaitable
    ) -> None:
        self.status_code = status_code
        self.func = func

    async def __call__(self,*args):
        return await self.func(*args)


    