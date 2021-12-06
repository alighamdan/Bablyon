import typing as t
import dataclasses

from bablyon.warrpers import Request
from bablyon.warrpers import Respone

@dataclasses.dataclass(init=True)
class Config:
    def __init__(
        self,
        middlewares:t.List[t.Awaitable]=[],
        request_class:t.Any=Request,
    ) -> None:
        self.middlewares = middlewares

        self.request_class = request_class

    def __repr__(self) -> str:
        return f'<Config ({[mw.__name__ for mw in self.middlewares]}) at 0x({id(self)})>'