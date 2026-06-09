import os

def delete_image_file(file_path):
    """Delete an image file at the given path if it exists."""
    if os.path.isfile(file_path):
        image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.svg', '.ico', '.tiff')
        if any(file_path.lower().endswith(ext) for ext in image_extensions):
            os.remove(file_path)
            return True
    return False

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        delete_image_file(sys.argv[1])
