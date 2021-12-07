def redirect(url:str,status_code:int=200):
    from bablyon.warrpers import Respone

    return Respone(
        body=f'<script> window.location.replace("{url}"); </script>',
        status=status_code,
        content_type='text/html'
    )