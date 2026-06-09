import tempfile


def write_unicode_to_temp_file(unicode_string):
    """Write a unicode string to a temporary file with UTF-8 encoding.

    Args:
        unicode_string: A unicode string to write to the file.

    Returns:
        The file path of the temporary file.
    """
    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', delete=False) as f:
        f.write(unicode_string)
        return f.name
