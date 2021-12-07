import re,io

def header_parser(headers:list,encode:str='utf-8'):
    return dict( (
        key.decode(encode),
        value.decode(encode)
    ) for key,value in headers )

def cookies_parser(cookies:str):
    if cookies == None:
        return {}
    return dict( (
        cookie.split('=')[0],
        cookie.split('=')[1]
    ) for cookie in cookies.replace(';','').split(' ') )

def parser_into_http_cookies(cookies:dict,encode:str='utf-8'):
    return (
        'Set-Cookie'.encode(encode),
        '; '.join(['='.join((
            key,
            value
        )) for key,value in cookies.items()]).encode(encode)
    )

def parser_into_http_headers(headers:dict,encode:str='utf-8'):
    return [(
        key.encode(encode),
        value.encode(encode),
    ) for key,value in headers.items()]

# This been taken from https://github.com/hzlmn/diy-async-web-framework#route-params
def format_pattern(path):
    if not re.search(r":(?P<param>\w+)", path):
        return path

    regex = r""
    last_pos = 0

    for match in re.finditer(r":(?P<param>\w+)", path):
        regex += path[last_pos: match.start()]
        param = match.group("param")
        regex += r"(?P<%s>\w+)" % param
        last_pos = match.end()

    return regex


def guess_content_type(body:str):
    if body.startswith(("<!DOCTYPE html>", "<!doctype html>", "<html>")):
        return "text/html"
    else:
        return "text/plain"

def guess_static_file_type(file:io.FileIO):
    file_type = file.name.split('.')[-1]
    if file_type == 'js':
        return 'application/javascript'
    elif file_type == 'css':
        return 'text/css'
    else:
        return 'text/plain'