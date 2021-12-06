from bablyon.router import Router,HTTPErrorRouter
from bablyon.serving import to_asgi
from bablyon.config import Config
from bablyon.warrpers import Request,Respone
from bablyon.utils import guess_content_type

import functools
import typing as t
import glob
import re

try:
    from ujson import dumps
except:
    from json import dumps

class Bablyon:
    def __init__(
        self,
        secret_key:str,
        routers:t.List[Router] = [],
        middlewares:list = [],
    ) -> None:
        self.routers = routers
        self.middlewares = middlewares
        self.secret_key = secret_key

        self.sessions = {}

    def mount(self,path:str,handler:t.Awaitable):
        for filename in glob.iglob(path + '**/**', recursive=True):
            path = filename.replace(u'\u005c','/').replace(path,'')

            self.routers.append(
                Router(
                    url=path,
                    func=handler
                )
            )

    async def build_asgi(self,request:Request):
        _request = Request(
            request.scope,
            request.body
        )

        for router in self.routers:
            if isinstance(router,HTTPErrorRouter):
                pass
            match = re.match(router.pattren, _request.path)

            if match is not None:
                if match.re.pattern != router.pattren:
                    pass

                bsession = _request.cookies.get('.bsession',False)
                if bsession != False:
                    if bsession not in self.sessions:
                        self.sessions[bsession] = {}
                
                request.match_info = match.groupdict()
                resp = await router(request)

                if isinstance(resp,Respone):
                    if resp.status != 200:
                        for router in self.routers:
                            if isinstance(router,HTTPErrorRouter):
                                if router.status_code == resp.status:
                                    resp = await router(request)

                if isinstance(resp,str):
                    return Respone(
                        body=resp,
                        content_type=guess_content_type(resp)
                    )

                elif isinstance(resp,dict):
                    return Respone(
                        body=dumps(resp),
                        content_type='application/json'
                    )
                
                return resp

    def __call__(self) -> t.Any:
        return to_asgi(
            self.build_asgi,
            config=Config(
                secret_key=self.secret_key,
                middlewares=self.middlewares
            )
        )