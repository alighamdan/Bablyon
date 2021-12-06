import bablyon
import re
import yarl

import typing as t

class LitServer:
    r"""
        LitServer the class that handle the `Requests` and dispatch the `Rotuers`
    """
    def __init__(
        self,
        app:t.Any
    ) -> None:
        from lit.application import Lit

        self.app:Lit = app
        self._param_regex = r"{(?P<param>\w+)}"

    # This been taken from https://github.com/hzlmn/diy-async-web-framework#route-params
    async def __call__(
        self,
        request:bablyon.Request
    ) -> None:
        from bablyon.warrpers import Respone,Request

        if request.session_token is not None:
            if request.session_token not in self.app.sessions:
                self.app.sessions[request.session_token] = {}

        for (pattren,method),handler in self.app.routers.items():
            match = re.match(pattren, yarl.URL(request.path).raw_path)

            if match is not None:
                if match.re.pattern == pattren:
                    match_info = match.groupdict() if match else {}

                    request._app = self.app
                    if method == request.method:
                        resp = await handler(request,**match_info)

                        if isinstance(resp,str):
                            return Respone(body=resp)
                        elif isinstance(resp,Respone):
                            return resp
                    else:
                        return Respone(body='Method not allowed')
                


            