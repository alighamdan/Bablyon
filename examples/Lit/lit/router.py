import typing as t
from bablyon.warrpers import Request

import re
import yarl

class LitRouter:
    def __init__(
        self,
        url:str,
        method:str,
        handler:t.Awaitable,
    ) -> None:
        from lit.utils import format_pattern
        
        self.pattren = format_pattern(url)
        self.url = url
        self.method = method
        self.handler = handler

    async def __call__(self, *args,**kwagrs) -> t.Any:
        return await self.handler(*args,**kwagrs)

    def __repr__(self) -> str:
        return f'<LitRouter ({self.url}) ({self.method}) at 0x({id(self)})>'