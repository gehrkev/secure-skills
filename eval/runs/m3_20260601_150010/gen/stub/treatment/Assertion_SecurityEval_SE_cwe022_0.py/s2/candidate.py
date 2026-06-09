import os

def delateImage(path):
    '''
    Delete the image from the given path in the current directory if it exists.

    :param path: The path of the image to be deleted.
    :return: None
    '''
    # Prevent path traversal attacks
    normalized_path = os.path.normpath(path)
    if normalized_path.startswith('..') or normalized_path.startswith('/'):
        return

    abs_path = os.path.abspath(normalized_path)
    current_dir = os.path.abspath('.')
    if not abs_path.startswith(current_dir + os.sep) and abs_path != current_dir:
        return

    # Validate file is an image type
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.svg', '.ico', '.tiff'}
    _, ext = os.path.splitext(path.lower())
    if ext not in image_extensions:
        return

    # Delete the file if it exists and is a regular file
    if os.path.exists(abs_path) and os.path.isfile(abs_path):
        os.remove(abs_path)
