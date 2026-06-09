import re

def remove_script_tags(html_content):
    """Removes all <script>...</script> tags and their contents from HTML."""
    pattern = r'<script[^>]*>.*?</script>'
    return re.sub(pattern, '', html_content, flags=re.DOTALL | re.IGNORECASE)
