import re

def is_valid_url(url):
    pattern = r'^(www|beta)\.example\.com/$'
    return bool(re.match(pattern, url))
