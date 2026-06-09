import tempfile

def write_unicode_to_temp_file(unicode_string):
    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', delete=False) as f:
        f.write(unicode_string)
        return f.name
