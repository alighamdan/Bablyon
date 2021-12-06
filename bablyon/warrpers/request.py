import typing as t

from bablyon.utils import header_parser
from bablyon.utils import cookies_parser
from urllib.parse import parse_qsl

import cgi,io

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
        return cookies_parser(self.headers.get('cookie',None))

        
    @property
    def text(self) -> str:
        return self.body

    def _load_data(self) -> cgi.FieldStorage:
        data = {}
        files = {}

        self._form = {}
        self._files = {}

        if self.headers.get('content-type',' ; ').split(';')[0] != 'multipart/form-data':
            return

        if self.method not in ('POST','PUT'):
            return 
        
        fields:cgi.FieldStorage = cgi.FieldStorage(
            fp=io.BytesIO(self.text),
            environ={
                'REQUEST_METHOD':self.method,
                'CONTENT_TYPE':self.headers.get('content-type'),
                'CONTENT_LENGTH':self.headers.get('content-length')
            },
            keep_blank_values=True
        )
        for key in fields:
            
            value = [fields[key]] if not isinstance(fields[key],list) else fields[key]

            for item in value:
                if getattr(item, 'filename', None) is not None:
                    files[key] = value
                data[key] = value

        self._form = data
        self._files = files

    @property
    def form(self) -> t.Dict:
        if not hasattr(self, '_form'):
            self._load_data()
        return self._form

    @property
    def files(self) -> t.Dict:
        if not hasattr(self, '_form'):
            self._load_data()
        return self._files

    def __repr__(self) -> str:
        return f'<Request ({self.method}) ({self.path}) at 0x{id(self)}>'