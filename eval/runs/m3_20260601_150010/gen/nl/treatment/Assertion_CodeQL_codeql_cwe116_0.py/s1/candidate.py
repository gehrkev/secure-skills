import re

def remove_script_tags(html):
    """Remove all script tags and their contents from HTML content."""
    return re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.IGNORECASE | re.DOTALL)
