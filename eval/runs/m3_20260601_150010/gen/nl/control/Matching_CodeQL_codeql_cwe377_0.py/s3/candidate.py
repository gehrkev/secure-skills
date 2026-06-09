import tempfile

def create_temp_file_with_unicode():
    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', delete=False) as f:
        f.write("Hello, 世界! 🌍")
        return f.name
