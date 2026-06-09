import re

def check_xyz_format(s):
    pattern = r'^[^.]+\.[^.]+\.[^.]+$'
    return bool(re.match(pattern, s))
