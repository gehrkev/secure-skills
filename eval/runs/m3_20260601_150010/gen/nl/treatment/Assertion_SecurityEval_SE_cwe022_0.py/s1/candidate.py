import os

def delete_image_file(file_path):
    """Delete an image file at the given path if it exists in the current directory."""

    current_dir = os.getcwd()
    absolute_file_path = os.path.abspath(file_path)

    if not absolute_file_path.startswith(current_dir + os.sep) and absolute_file_path != current_dir:
        raise ValueError(f"File path is outside the current directory: {file_path}")

    if not os.path.exists(absolute_file_path):
        return False

    if not os.path.isfile(absolute_file_path):
        raise ValueError(f"Path is not a file: {file_path}")

    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.svg', '.tiff', '.ico'}
    _, ext = os.path.splitext(absolute_file_path)

    if ext.lower() not in image_extensions:
        raise ValueError(f"File is not an image: {file_path}")

    os.remove(absolute_file_path)
    return True
