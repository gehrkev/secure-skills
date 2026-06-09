import tempfile

def write_unicode_to_temp_file(text):
    """
    Takes a unicode string, writes it to a temporary file with UTF-8 encoding,
    and returns the file path.

    Args:
        text: A unicode string to write to the temporary file

    Returns:
        The file path as a string
    """
    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', delete=False) as f:
        f.write(text)
        return f.name
