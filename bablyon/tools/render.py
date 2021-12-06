from jinja2 import Template

async def render(path:str,*args,**params):
    from bablyon.warrpers import Respone

    template = Template(
        open(path,'r').read(),
        enable_async=True
    )
    body = await template.render_async(*args,**params)

    return Respone(
        body=body,
        content_type='text/html'
    )