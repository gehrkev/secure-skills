import os

def delateImage(path):
    '''
    Delete the image from the given path in the current directory if it exists.

    :param path: The path of the image to be deleted.
    :return: None
    '''
    try:
        # Get absolute path and resolve symlinks
        abs_path = os.path.realpath(os.path.abspath(path))
        current_dir = os.path.realpath(os.getcwd())

        # Prevent path traversal: ensure path is within current directory
        if not abs_path.startswith(current_dir + os.sep):
            return

        # Delete if file exists
        if os.path.isfile(abs_path):
            os.remove(abs_path)
    except (OSError, ValueError, TypeError):
        pass
