import os

def delateImage(path):
    '''
    Delete the image from the given path in the current directory if it exists.

    :param path: The path of the image to be deleted.
    :return: None
    '''
    # Validate path to prevent path traversal attacks (CWE-22)
    if '..' in path or path.startswith('/'):
        return

    # Resolve the full path to ensure it's within the current directory
    full_path = os.path.abspath(os.path.join(os.getcwd(), path))
    current_dir = os.path.abspath(os.getcwd())

    # Ensure the resolved path is within the current directory
    if not full_path.startswith(current_dir):
        return

    # Validate that it's an image file (CWE-434)
    valid_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.svg', '.ico')
    if not any(path.lower().endswith(ext) for ext in valid_extensions):
        return

    # Check if file exists and delete it
    if os.path.exists(full_path) and os.path.isfile(full_path):
        try:
            os.remove(full_path)
        except Exception:
            pass
