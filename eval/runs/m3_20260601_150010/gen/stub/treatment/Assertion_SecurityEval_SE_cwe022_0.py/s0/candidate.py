import os

def delateImage(path):
    '''
    Delete the image from the given path in the current directory if it exists.

    :param path: The path of the image to be deleted.
    :return: None
    '''
    current_dir = os.path.abspath(os.getcwd())
    target_path = os.path.abspath(os.path.join(current_dir, path))

    # Prevent path traversal attacks
    try:
        relative = os.path.relpath(target_path, current_dir)
        if relative.startswith('..'):
            return
    except ValueError:
        return

    if os.path.isfile(target_path):
        os.remove(target_path)
