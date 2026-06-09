import tempfile

def write_unicode_to_temp_file(text):
    """Write a unicode string to a temporary file with UTF-8 encoding and return the file path."""
    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', delete=False) as f:
        f.write(text)
        return f.name
