import re

def check_url_format(url):
    """Check if a URL has the format (www|beta).example.com/"""
    pattern = r'^(www|beta)\.example\.com\/'
    return bool(re.match(pattern, url))
