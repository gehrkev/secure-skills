def open_file(path):
    """
    Tries to open a file at the given path and returns the file object
    if it opens successfully, or None if it fails.

    Args:
        path: The file path to open

    Returns:
        The file object if successful, None if an error occurs
    """
    try:
        return open(path, 'r')
    except Exception:
        return None
