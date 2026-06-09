import re

def remove_script_tags(html_content):
    """
    Removes all script tags and their contents from HTML content.

    Args:
        html_content: A string containing HTML content

    Returns:
        A string with all <script>...</script> tags removed
    """
    pattern = r'<script[^>]*>.*?</script>'
    result = re.sub(pattern, '', html_content, flags=re.IGNORECASE | re.DOTALL)
    return result
