from bablyon.router import Router
from bablyon.serving import to_asgi
from bablyon.config import Config
from bablyon.warrpers import Request,Respone
from bablyon.utils import guess_content_type

import typing as t
import glob
import os
import re

try:
    from ujson import dumps
except:
    from json import dumps

class Bablyon:
    def __init__(
        self,
        routers:t.List[Router] = [],
        middlewares:list = [],
    ) -> None:
        self.routers = routers
        self.middlewares = middlewares

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
        for router in self.routers:
            match = re.match(router.pattren, request.path)

            if match is not None:
                if match.re.pattern != router.pattren:
                    pass
            
                request.match_info = match.groupdict()
                resp = await router.func(request)

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
                middlewares=self.middlewares
            )
        )