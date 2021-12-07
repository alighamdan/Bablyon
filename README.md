# Bablyon 🐍
A small ASGI web framework that you can make asynchronous web applications using [`uvicorn`](https://github.com/encode/uvicorn) with using few lines of code

# Installation 
 `python -m pip install git+https://github.com/xArty4/Bablyon`

# Exmaple 
```py
from bablyon.application import Bablyon
from bablyon.router import Router
from bablyon.staticfile import StaticFile


async def hello(request):
    print(request.json)

    return f'at {request.path}'
    
routers = [
    Router('/hello',hello)
]

app = Bablyon(
    secret_key='hello',
    routers=routers,
    middlewares=[]
)

app.mount('./static',StaticFile('./static'))

if __name__ == '__main__':
    from uvicorn.main import run
    
    run(
        f'test3:app',
        host='localhost',
        port=5000,
        debug=True
    )

```
# Author
- [xArty](https://github.com/xArty4)

# To Do
- Custom request class ✅
- Add Jinjia2 to the box ✅
- Full session ✅
- Add security to the cookies ✅
- Add Exceptions to the box ❌
- Add routing to the box ✅
- Add static files support ✅ 
- Add middleware support ✅
- Add HTTP Exceptions ✅