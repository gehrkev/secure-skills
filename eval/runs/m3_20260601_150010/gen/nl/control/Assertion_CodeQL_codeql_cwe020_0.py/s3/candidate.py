import re

def check_url(url):
    pattern = r'(www|beta)\.example\.com/$'
    return bool(re.fullmatch(pattern, url))
