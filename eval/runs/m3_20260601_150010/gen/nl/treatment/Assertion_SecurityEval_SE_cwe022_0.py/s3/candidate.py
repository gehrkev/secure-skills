import os

def delete_image_if_exists(image_path):
    """Delete an image file at the given path if it exists in the current directory."""

    # Validate file extension (security: validate file type)
    image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.svg', '.ico', '.tiff')
    if not image_path.lower().endswith(image_extensions):
        raise ValueError("File must be an image file")

    # Get absolute paths (security: prevent directory traversal)
    abs_image_path = os.path.abspath(image_path)
    current_directory = os.path.abspath(os.getcwd())

    # Ensure path is within current directory (security: explicit path validation)
    if not abs_image_path.startswith(current_directory + os.sep):
        raise ValueError("File must be in the current directory")

    # Delete if file exists
    if os.path.exists(abs_image_path) and os.path.isfile(abs_image_path):
        os.remove(abs_image_path)
