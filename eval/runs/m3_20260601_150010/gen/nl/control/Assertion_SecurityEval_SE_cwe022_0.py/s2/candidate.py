import os

def delete_image_if_exists(path):
    """Delete an image file at the given path if it exists."""
    if os.path.exists(path):
        os.remove(path)
