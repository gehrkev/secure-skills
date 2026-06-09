import re

def is_valid_url(url):
    """Check if a given URL matches the pattern (www|beta).example.com/"""
    pattern = r'^(www|beta)\.example\.com/$'
    return bool(re.match(pattern, url))
