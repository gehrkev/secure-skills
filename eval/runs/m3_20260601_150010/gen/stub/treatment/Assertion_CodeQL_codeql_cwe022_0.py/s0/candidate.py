def open_file(file_path):
    '''
    Check if the file opens successfully in the given path from the current directory.

    :param file_path: The path to the file to open.
    :return: The file object if the file opens successfully, None otherwise.
    '''
    import os

    try:
        # Prevent path traversal attacks by ensuring the file is within current directory
        current_dir = os.path.abspath('.')
        target_path = os.path.abspath(file_path)

        # Check if target is within current directory
        if not target_path.startswith(current_dir + os.sep):
            return None

        # Open and return the file
        return open(file_path, 'r')
    except Exception:
        return None
