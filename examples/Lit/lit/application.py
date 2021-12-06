import typing as t

from lit.router import LitRouter

class Lit:
    r""""""
    def __init__(
        self,
    ) -> None:
        from lit.server import LitServer

        self.server = LitServer(self)
        self.routers:t.Dict[t.Tuple[str,str],LitServer] = {}

    def route(
        self,
        path:str,
        method:str,
    ):
        def deco(func:t.Awaitable):
            from lit.utils import format_pattern
            self.routers[(format_pattern(path),method)] = LitRouter(url=path,method=method,handler=func)
        return deco

    def __call__(self) -> t.Any:
        from bablyon import to_asgi

        return to_asgi(self.server.__call__)