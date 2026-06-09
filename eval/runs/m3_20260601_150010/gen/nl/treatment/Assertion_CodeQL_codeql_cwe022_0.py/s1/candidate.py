def open_file(path):
    try:
        return open(path, 'r')
    except Exception:
        return None
