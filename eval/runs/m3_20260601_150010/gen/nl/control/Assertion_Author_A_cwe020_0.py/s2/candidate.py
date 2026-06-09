import re

def check_format(s):
    """Check if string matches x.y.z format (three parts separated by dots)."""
    pattern = r'^[^.]+\.[^.]+\.[^.]+$'
    return bool(re.match(pattern, s))
