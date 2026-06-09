import tempfile

def create_temp_file_with_unicode():
    """Create a temporary file with UTF-8 encoding, write a unicode string to it, and return the file path."""
    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', delete=False) as f:
        f.write('Hello, 世界! 🌍')
        return f.name

if __name__ == '__main__':
    file_path = create_temp_file_with_unicode()
    print(f"Temporary file created at: {file_path}")
