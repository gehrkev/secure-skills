import re

def check_url_format(url):
    pattern = r'^(www|beta)\.example\.com/$'
    return bool(re.match(pattern, url))
