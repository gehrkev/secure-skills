import re

def check_version_format(s):
    pattern = r'^[^.]+\.[^.]+\.[^.]+$'
    return bool(re.match(pattern, s))
