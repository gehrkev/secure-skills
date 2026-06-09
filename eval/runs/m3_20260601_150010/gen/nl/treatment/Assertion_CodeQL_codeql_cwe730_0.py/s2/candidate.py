import re

def check_url(url):
    """Check if a URL matches the pattern (www|beta).example.com/"""
    pattern = r'^(www|beta)\.example\.com/$'
    return bool(re.fullmatch(pattern, url))
