import typing as t
import secrets as s

from bablyon.handlers import RequestBaseHandler
from bablyon.config import Config

def asgi_application(config:Config=Config()):
    def deco(func:t.Awaitable):
        async def warrper(scope, receive, send):
            return await RequestBaseHandler(config).__call__(func,scope,receive,send)
    
        warrper.__module__ = func.__module__
        warrper.__name__ = func.__name__
        warrper.bablyon_handler = func
        return warrper
    return deco

def to_asgi(func:t.Awaitable,config:Config):
    @asgi_application(config)
    async def warrper(request):
        return await func(request)
    return warrper

def run_simple(
    app:t.Awaitable,
    **kwagrs
):
    from uvicorn.main import run

    run(
        app=app,
        **kwagrs
    )
