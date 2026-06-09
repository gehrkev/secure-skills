import os

def delete_image_if_exists(file_path):
    """Delete an image file at the given path if it exists in the current directory."""

    # Allowed image file extensions
    image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.svg', '.ico', '.tiff', '.tif')

    # Validate file extension to ensure it's an image
    if not any(file_path.lower().endswith(ext) for ext in image_extensions):
        return False

    # Get absolute paths
    current_dir = os.path.abspath(os.getcwd())
    file_abs_path = os.path.abspath(file_path)

    # Check if file is within current directory (prevent path traversal)
    try:
        rel_path = os.path.relpath(file_abs_path, current_dir)
        if rel_path.startswith('..'):
            return False
    except ValueError:
        # Different drives on Windows
        return False

    # Delete the file if it exists
    if os.path.exists(file_abs_path):
        try:
            os.remove(file_abs_path)
            return True
        except OSError:
            return False

    return False

if __name__ == "__main__":
    image_path = input("Enter the image file path: ")
    if delete_image_if_exists(image_path):
        print(f"Image deleted: {image_path}")
    else:
        print(f"Failed to delete image or file does not exist: {image_path}")
