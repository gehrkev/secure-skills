import re

def check_version_format(s):
    """Check if a string matches the format x.y.z (three parts separated by dots)."""
    pattern = r'^[^.]+\.[^.]+\.[^.]+$'
    return bool(re.match(pattern, s))
