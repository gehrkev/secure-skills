import re

def check_xyz_format(s):
    """Check if a string matches the format x.y.z (three parts separated by dots)."""
    pattern = r'^(\w+)\.(\w+)\.(\w+)$'
    return bool(re.match(pattern, s))
