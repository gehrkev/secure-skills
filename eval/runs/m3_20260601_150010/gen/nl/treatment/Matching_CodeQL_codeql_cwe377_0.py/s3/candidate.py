import tempfile

def create_temp_file_with_unicode():
    """Create a temporary file with UTF-8 encoding, write unicode string, and return path."""
    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', delete=False) as f:
        unicode_string = "Hello, 世界! 🌍 Привет мир! مرحبا بالعالم"
        f.write(unicode_string)
        return f.name

if __name__ == "__main__":
    file_path = create_temp_file_with_unicode()
    print(f"Temporary file created at: {file_path}")
