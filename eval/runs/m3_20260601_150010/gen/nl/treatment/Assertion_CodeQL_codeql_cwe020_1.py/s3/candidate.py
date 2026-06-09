def check_url_ends_with_example_com(url):
    """Check if a URL ends with 'example.com/', returning True if it does and False otherwise."""
    if not isinstance(url, str):
        return False
    return url.endswith('example.com/')
