# Bablyon 🐍
A small ASGI web framework that you can make asynchronous web applications using [`uvicorn`](https://github.com/encode/uvicorn) with using few lines of code

# Exmaple 
```py
import bablyon

@bablyon.to_asgi
async def application(request:bablyon.Request):
    return bablyon.Respone(
        body='Hello from Babylon'
    )

if __name__ == '__main__':
    from bablyon import run_simple
    from platform import python_version
    run_simple(
        app=application,
        host='localhost',
        port=5000,
        debug=True,
        headers=[['Python',f'{python_version()}']]
    )
```
# Author
- [xArty](https://github.com/xArty4)