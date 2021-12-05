import typing as t

from bablyon.utils import header_parser
from bablyon.utils import cookies_parser
from urllib.parse import parse_qsl

class Request:
    r"""
        Request class a paraser for the `receive` args in the ASGI handler
        a way to parase the data from the `receive` in the ASGI handler   
        and make it more readable to the developer

        Attributes
        ----------
        method : `str`
            Return the request method
        version : `str`
            Return the version of the request
        path : `str`
            Return the path or the url of the request
        args : `Dict`
            Return the args that are in the end of the url
        headers : `Dict`
            Return the headers of the request
        text : `str`
            Return the body of the request
        json : `Dict`
            Decode the body and return it as Dict
    """
    def __init__(
        self,
        scope:t.Dict[str,t.Union[bytes,str]],
        body:str
    ) -> None:

        self.scope = scope
        self.body = body

        self.decode = 'utf-8'

    @property
    def client(self) -> t.Tuple[str,str]:
        return self.scope.get('client')

    @property
    def server(self) -> t.Tuple[str,str]:
        return self.scope.get('server')

    @property
    def method(self) -> str:
        return self.scope.get('method',None)
    
    @property
    def version(self) -> str:
        return f'HTTP/{self.scope.get("http_version",None)}'

    @property
    def path(self) -> str:
        return self.scope.get('path',None)

    @property
    def args(self) -> t.Dict:
        return parse_qsl(
            self.scope.get('query_string','').decode('utf-8')
        )

    @property
    def headers(self) -> t.Dict:
        return header_parser(
            self.scope.get('headers',[(b'',b'')]),
            self.decode
        )

    @property
    def cookies(self) -> t.Dict:
        return cookies_parser(self.headers.get('cookie',''))

    @property
    def session_token(self) -> str:
        return self.cookies.get('.bablyon-session',None)
        
    @property
    def text(self) -> str:
        return self.body

    def __repr__(self) -> str:
        return f'<Request ({self.method}) ({self.path}) at 0x{id(self)}>'