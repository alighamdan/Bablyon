import typing as t
import dataclasses

@dataclasses.dataclass(init=True)
class Config:
    def __init__(
        self,
        middlewares:t.List[t.Awaitable]=[]
    ) -> None:
        self.middlewares = middlewares

    def __repr__(self) -> str:
        return f'<Config ({[mw.__name__ for mw in self.middlewares]}) at 0x({id(self)})>'