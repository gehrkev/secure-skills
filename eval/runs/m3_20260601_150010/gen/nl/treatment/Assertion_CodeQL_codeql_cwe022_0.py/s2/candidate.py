def open_file_safe(path):
    try:
        return open(path, 'r')
    except (FileNotFoundError, PermissionError, IsADirectoryError, IOError, OSError):
        return None
