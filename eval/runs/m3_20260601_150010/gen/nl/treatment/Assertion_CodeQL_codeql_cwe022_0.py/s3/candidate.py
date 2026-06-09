def open_file(path):
    """
    Try to open a file at the given path and return the file object.

    Returns the file object if the file opens successfully, or None if it fails.
    """
    try:
        return open(path, 'r')
    except (FileNotFoundError, IOError, OSError, PermissionError):
        return None
