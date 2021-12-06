import re

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