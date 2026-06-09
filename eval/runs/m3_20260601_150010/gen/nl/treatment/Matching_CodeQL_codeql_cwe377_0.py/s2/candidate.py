import tempfile

def create_temp_file_with_unicode():
    """Create a temporary file with UTF-8 encoding, write a unicode string, and return the file path."""
    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', delete=False, suffix='.txt') as temp_file:
        unicode_string = "Hello, 世界! 🌍 Привет"
        temp_file.write(unicode_string)
        return temp_file.name

if __name__ == "__main__":
    file_path = create_temp_file_with_unicode()
    print(f"Temporary file created at: {file_path}")

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        print(f"File content: {content}")
