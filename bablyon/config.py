import typing as t
import dataclasses
import secrets as s

from bablyon.warrpers import Request
from bablyon.warrpers import Respone


@dataclasses.dataclass(init=True)
class Config:
    def __init__(
        self,
        secret_key:str=None,
        middlewares:t.List[t.Awaitable]=[],
        request_class:t.Any=Request,
        encoding:str='utf-8'
    ) -> None:
        self.secret_key = secret_key if secret_key is not None else s.token_hex(16)
        self.encoding = encoding
        self.middlewares = middlewares
        self.request_class = request_class

    def __repr__(self) -> str:
        return f'<Config (*****) ({self.encoding}) at 0x({id(self)})>'