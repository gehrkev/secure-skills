import re

def check_format(s):
    """Check if a string matches the format x.y.z"""
    pattern = r'^[^.]+\.[^.]+\.[^.]+$'
    return bool(re.match(pattern, s))
