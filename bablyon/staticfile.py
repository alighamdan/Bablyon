import typing as t

from bablyon.warrpers import Respone
from bablyon.warrpers import Request
from bablyon.utils import guess_static_file_type

class StaticFile:
    def __init__(
        self,
        dir:str,
    ) -> None:
        self.dir = dir

    async def __call__(self,request:Request) -> t.Any:
        file_io = open(f'{self.dir}{request.path}','r')
        return Respone(
            body=file_io.read(),
            content_type=guess_static_file_type(file_io)
        )