import re

def remove_script_tags(html_content):
    """
    Removes all script tags and their contents from HTML content.

    Args:
        html_content: A string containing HTML content

    Returns:
        The string with all <script>...</script> tags stripped out
    """
    pattern = r'<script\b[^>]*>.*?</script>'
    return re.sub(pattern, '', html_content, flags=re.IGNORECASE | re.DOTALL)
