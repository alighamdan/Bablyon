import typing as t
import asyncio as a

from bablyon.warrpers import Request
from bablyon.warrpers import Respone
from bablyon.config import Config

class HTTPRequestHandler:


    def __init__(
        self,
        send:t.Awaitable,
        recv:t.Awaitable,
        config:Config,
    ) -> None:
        self.send = send
        self.recv = recv
        self.config = config


    async def __call__(
        self,
        emit:t.Awaitable,
        request:Request
    ) -> t.Any:

        if self.config.middlewares != []:
            for mw in self.config.middlewares:
                mw_resp = await mw(request)

                if isinstance(mw_resp,Respone):
                    for i in mw_resp._to_list():
                        await self.send(i)
                    return
                else:
                    pass

        resp = await emit(request)

        if isinstance(resp,Respone):
            for i in resp._to_list():
                await self.send(i)

class RequestBaseHandler:


    def __init__(
        self,
        config:Config
    ) -> None:
        self.config = config

    
    async def __call__(
        self,
        emit:t.Awaitable,
        scope:t.Dict[str,t.Union[bytes,str]], 
        receive:t.Callable, 
        send:t.Callable
    ) -> t.Any:

        self.recv = receive
        self.send = send

        if a.iscoroutinefunction(emit) is False:
            return

        if scope["type"] == "lifespan.startup": await send({"type": "lifespan.startup.complete"})

        elif scope["type"] == "lifespan.shutdown": await send({"type": "lifespan.shutdown.complete"})


        elif scope["type"] == "http": 
            body = await self.recv()
            body = body.get('body')
            
            await HTTPRequestHandler(
                self.send,
                self.recv,
                self.config
            ).__call__(
                emit,
                Request(
                    scope,
                    body=body
                )
            )