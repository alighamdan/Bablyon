import lit

app = lit.Lit()

@app.route('/api/blog/:hello_world/:wewe/tre',method='GET')
async def hello(request:lit.Request,hello_world,wewe):
    return "Hello"

@app.route('/api/hego',method='GET')
async def hello2(request:lit.Request):
    return "qeqw" 

if __name__ == '__main__':
    from uvicorn.main import run

    run(
        f'test:app',
        host='localhost',
        port=5000,
        debug=True
    )