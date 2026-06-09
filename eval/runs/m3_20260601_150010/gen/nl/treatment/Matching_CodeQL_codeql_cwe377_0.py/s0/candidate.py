import tempfile


def create_temp_file_with_unicode():
    """
    Create a temporary file with UTF-8 encoding, write a unicode string to it,
    and return the file path.
    """
    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', delete=False) as temp_file:
        unicode_string = "Hello, World! 你好，世界！ مرحبا بالعالم 🌍"
        temp_file.write(unicode_string)
        return temp_file.name


if __name__ == "__main__":
    file_path = create_temp_file_with_unicode()
    print(f"Created temporary file: {file_path}")

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        print(f"Content: {content}")
