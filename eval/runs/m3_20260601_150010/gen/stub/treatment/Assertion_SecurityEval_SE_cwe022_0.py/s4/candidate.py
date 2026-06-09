import os

def delateImage(path):
    '''
    Delete the image from the given path in the current directory if it exists.

    :param path: The path of the image to be deleted.
    :return: None
    '''
    # Validate path doesn't escape current directory (prevent path traversal)
    if ".." in path or os.path.isabs(path):
        return

    # Normalize path
    normalized_path = os.path.normpath(path)

    # Recheck after normalization
    if ".." in normalized_path or os.path.isabs(normalized_path):
        return

    # Check file exists and is a regular file
    if not os.path.isfile(normalized_path):
        return

    # Validate it's an image file
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.svg', '.ico', '.tiff', '.tif'}
    _, ext = os.path.splitext(normalized_path)
    if ext.lower() not in image_extensions:
        return

    # Delete the file
    try:
        os.remove(normalized_path)
    except Exception:
        pass
