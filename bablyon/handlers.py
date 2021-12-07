import typing as t
import asyncio as a
import secrets as s

from bablyon.warrpers import Request
from bablyon.warrpers import Respone
from bablyon.config import Config

from bablyon.security import encrypt


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
        scope:t.Dict[str,t.Union[bytes,str]],
        body:str
    ) -> t.Any:

        _request = Request(
            scope,
            body
        )
        request = self.config.request_class(
            scope,
            body
        )

        if _request.cookies.get('.bsession',False) == False:
            self.token = encrypt(
                s.token_hex(16),
                self.config.secret_key,
                self.config.encoding
            )
        
        if self.config.middlewares != []:
            for mw in self.config.middlewares:
                mw_resp = await mw(request)

                if mw_resp:
                    await self._send(mw_resp)
                    return
                else:
                    pass

        resp = await emit(request)
        await self._send(resp)

    async def _send(self,resp:t.List):
        if isinstance(resp,Respone):
            if hasattr(self,'token'):
                resp.add_cookie('.bsession',self.token)
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
                scope,
                body
            )