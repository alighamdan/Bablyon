from hashlib import blake2b
from hmac import compare_digest

def encrypt(cookie:str,secret_key:str,encode:str='utf-8'):
    return blake2b(
        cookie.encode(encode),
        digest_size=16,
        key=secret_key.encode(encode)
    ).hexdigest()

def verfiy(user_cookie:str,computer_cookie:str,secret_key:str):
    return encrypt(user_cookie,secret_key) == computer_cookie