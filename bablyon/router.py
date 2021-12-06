import re
import typing as t

from bablyon.utils import format_pattern
from asyncio import iscoroutinefunction

class Router:
    def __init__(
        self,
        url:str,
        func:t.Awaitable
    ) -> None:
        self.url = url
        self.pattren = format_pattern(url)
        self.func = func

    async def __call__(self,*args):
        if iscoroutinefunction(self.func):
            return await self.func