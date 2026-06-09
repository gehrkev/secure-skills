import re

def remove_script_tags(html_content):
    """
    Removes all script tags and their contents from HTML content using regex.

    Args:
        html_content (str): HTML content as a string

    Returns:
        str: HTML content with all script tags and their contents removed
    """
    pattern = r'<script\b[^>]*>.*?</script>'
    return re.sub(pattern, '', html_content, flags=re.DOTALL | re.IGNORECASE)
