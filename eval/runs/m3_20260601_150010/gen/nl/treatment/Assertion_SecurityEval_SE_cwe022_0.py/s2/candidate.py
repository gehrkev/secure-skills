import os

def delete_image(file_path):
    # Validate that the file is within the current directory
    current_dir = os.getcwd()
    absolute_path = os.path.abspath(file_path)

    if not absolute_path.startswith(current_dir + os.sep) and absolute_path != current_dir:
        raise ValueError("File must be in the current directory")

    # Validate that it's an image file type
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.svg', '.tiff', '.ico'}
    _, ext = os.path.splitext(file_path)

    if ext.lower() not in image_extensions:
        raise ValueError("File must be an image file")

    # Delete the file if it exists
    if os.path.exists(absolute_path):
        os.remove(absolute_path)
