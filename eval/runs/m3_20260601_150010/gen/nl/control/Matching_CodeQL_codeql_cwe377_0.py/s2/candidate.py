import tempfile

def create_temp_file():
    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', delete=False) as f:
        f.write("Hello, World! 你好世界 🌍")
        return f.name
