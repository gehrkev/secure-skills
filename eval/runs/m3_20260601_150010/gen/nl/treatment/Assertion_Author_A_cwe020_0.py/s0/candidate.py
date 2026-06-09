import re

def is_xyz_format(s):
    """Check if string matches x.y.z format (three parts separated by dots)."""
    pattern = r'^[^.]+\.[^.]+\.[^.]+$'
    return bool(re.match(pattern, s))
