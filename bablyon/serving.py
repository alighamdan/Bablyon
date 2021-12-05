import typing as t
import secrets as s

def to_asgi(func:t.Awaitable):
    async def warrper(scope, receive, send):
        return await bablyon_handler(func,scope,receive,send)
    
    warrper.__module__ = func.__module__
    warrper.__name__ = func.__name__
    warrper.bablyon_handler = func
    return warrper

async def bablyon_handler(handler,scope, receive, send):
    from bablyon.warrpers import Request
    from bablyon.warrpers import Respone

    if scope["type"] == "lifespan.startup":
        await send({"type": "lifespan.startup.complete"})

    elif scope["type"] == "lifespan.shutdown": 
        await send({"type": "lifespan.shutdown.complete"})

    elif scope["type"] != "http":
        return

    recv = await receive()
    request = Request(scope,recv.get('body'))
    resp:Respone = await handler(request)

    if '.bablyon-session' not in request.cookies:
        resp.add_cookie('.bablyon-session',s.token_hex(6))
    
    if resp is not None:
        for i in resp._to_list():
            await send(i)
    
    else:
        for i in Respone(body='There is no body returned in this request')._to_list():
            await send(i)


def run_simple(
    app:t.Awaitable,
    **kwagrs
):
    from uvicorn import __version__ as Uvicorn_Version
    from . import __verison__ as Bablyon_Version
    from platform import python_version as Python_Version

    from uvicorn.main import run

    run(
        f'{app.__module__}:{app.__name__}',
        **kwagrs
    )
