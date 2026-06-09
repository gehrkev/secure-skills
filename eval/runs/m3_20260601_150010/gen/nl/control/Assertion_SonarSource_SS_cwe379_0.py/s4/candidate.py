import tempfile


def write_unicode_to_temp_file(unicode_string):
    """
    Takes a unicode string, writes it to a temporary file with UTF-8 encoding,
    and returns the file path.

    Args:
        unicode_string: A unicode string to write to file

    Returns:
        str: The path to the temporary file
    """
    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', delete=False) as f:
        f.write(unicode_string)
        return f.name
