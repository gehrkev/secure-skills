import re

def remove_script_tags(html_content):
    """Remove all script tags and their contents from HTML content."""
    return re.sub(r'<script[^>]*>.*?</script>', '', html_content, flags=re.DOTALL | re.IGNORECASE)
