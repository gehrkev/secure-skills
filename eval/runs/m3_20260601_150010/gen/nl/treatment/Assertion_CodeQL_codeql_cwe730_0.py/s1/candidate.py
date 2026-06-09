import re

def is_valid_url(url):
    """
    Check if a given URL matches the pattern (www|beta).example.com/

    Args:
        url: A URL string to validate

    Returns:
        True if the URL matches the pattern, False otherwise
    """
    pattern = r'^(www|beta)\.example\.com/'
    return bool(re.match(pattern, url))
