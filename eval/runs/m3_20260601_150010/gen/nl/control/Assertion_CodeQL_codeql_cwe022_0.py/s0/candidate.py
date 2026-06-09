def open_file(path):
    try:
        return open(path)
    except:
        return None
