import re

def remove_script_tags(html_content):
    """Remove all script tags and their contents from HTML content."""
    pattern = r'<script[^>]*>.*?</script>'
    return re.sub(pattern, '', html_content, flags=re.IGNORECASE | re.DOTALL)
