import tempfile

def create_temp_file_with_unicode():
    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', delete=False) as f:
        unicode_string = "Hello, 世界! 🌍"
        f.write(unicode_string)
        return f.name

if __name__ == "__main__":
    file_path = create_temp_file_with_unicode()
    print(file_path)
