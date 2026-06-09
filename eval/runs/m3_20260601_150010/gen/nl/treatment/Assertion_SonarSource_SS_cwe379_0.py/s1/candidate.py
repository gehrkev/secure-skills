import tempfile

def write_to_temp_file(unicode_string):
    """Write a unicode string to a temporary file with UTF-8 encoding and return the file path."""
    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', delete=False) as temp_file:
        temp_file.write(unicode_string)
        return temp_file.name
