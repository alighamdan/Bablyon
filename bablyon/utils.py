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
