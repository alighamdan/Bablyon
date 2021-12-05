import typing as t

from bablyon.utils import parser_into_http_headers
from bablyon.utils import parser_into_http_cookies


class Respone:
    r"""
        Respone class is a way to interpretation the raw 
         
        Attributes
        ----------
        body : `str`
            Return the body that you want to send
        status : `str`
            Return the status you want to send
        headers : `Dict`
            Return the headers you want to send
        cookies : `Dict`
            Return the cookies you want to send
    """
    def __init__(
        self,
        body:str,
        status:str=200,
        content_type:str="text/plain",
        headers:t.Dict[str,str]={},
        cookeis:t.Dict[str,str]={},
    ) -> None:
        self._body = body
        self._status = status
        self._headers = headers
        self._content_type = content_type
        self._cookies = cookeis

        self._headers['Content-Type'] = content_type

        self.encode = 'utf-8'

    @property
    def body(self) -> str:
        return self._body

    @property
    def status(self) -> str:
        return self._status

    @property
    def headers(self) -> t.Dict[str,str]:
        return self._headers

    @property
    def content_type(self) -> str:
        return self._content_type

    @property
    def cookies(self) -> t.Dict[str,str]:
        return self._cookies

    def add_body(self,body:str) -> str:
        return self.body + body

    def add_header(self,key:str,value:str) -> None:
        self.headers[key] = value

    def add_cookie(self,key:str,value:str) -> None:
        self.cookies[key] = value

    
    def _parase_headers(self) -> t.List:
        if self.cookies != {}:
            return [
                [(
                    key,
                    value
                ) for key,value in parser_into_http_headers(
                    self.headers,
                    self.encode
                ) ][0], 
                parser_into_http_cookies(
                    self.cookies,
                    self.encode)
                ]
        else:
            return parser_into_http_headers(
                self.headers,
                self.encode
            )
            

    def _to_list(self) -> list:
        return [
            {
                'type'    : 'http.response.start',
                'status'  : self.status,
                'headers' : self._parase_headers()
            },
            {
                'type': 'http.response.body',
                'body': self.body.encode(self.encode)
            }
        ]

    def __repr__(self) -> str:
        return f'<Respone ({self.body}) ({self.headers}) at 0x{id(self)}>'