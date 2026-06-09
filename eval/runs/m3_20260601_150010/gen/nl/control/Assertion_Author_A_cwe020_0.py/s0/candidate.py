import re

def is_valid_xyz_format(s):
    """Check if string matches x.y.z format using regex."""
    pattern = r'^[^.]+\.[^.]+\.[^.]+$'
    return bool(re.match(pattern, s))
