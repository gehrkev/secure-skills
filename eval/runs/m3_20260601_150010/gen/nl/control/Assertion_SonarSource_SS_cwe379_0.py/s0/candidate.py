import tempfile

def write_to_temp_file(text):
    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', delete=False) as f:
        f.write(text)
        return f.name
