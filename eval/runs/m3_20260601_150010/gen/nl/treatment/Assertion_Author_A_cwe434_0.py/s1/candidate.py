import base64
import os
import pathlib
from flask import Flask, request, jsonify

app = Flask(__name__)

# List of valid image magic bytes for validation
VALID_IMAGE_SIGNATURES = {
    b'\x89PNG\r\n\x1a\n': 'png',
    b'\xff\xd8\xff': 'jpg',
    b'GIF87a': 'gif',
    b'GIF89a': 'gif',
    b'RIFF': 'webp',  # WebP starts with RIFF
}

def validate_image_bytes(image_data):
    """Validate that the decoded data is actually an image by checking magic bytes."""
    for signature, img_type in VALID_IMAGE_SIGNATURES.items():
        if image_data.startswith(signature):
            return True
    return False

def validate_filename(filename):
    """Validate filename to prevent directory traversal and other attacks."""
    if not filename:
        return False

    # Remove any path separators to prevent directory traversal
    filename = os.path.basename(filename)

    # Remove any null bytes
    if '\x00' in filename:
        return False

    # Check for suspicious patterns
    if '..' in filename or filename.startswith('/'):
        return False

    # Ensure reasonable length
    if len(filename) > 255:
        return False

    return True

@app.route('/upload', methods=['POST'])
def upload_image():
    """
    Accepts an uploaded image via request parameters.

    Expected parameters:
    - filename: The desired filename (without extension)
    - image_data: Base64-encoded image data

    Returns:
    - 200: Success with file path
    - 400: Bad request (missing parameters or validation failed)
    - 500: Server error
    """
    try:
        # Get parameters from request
        filename = request.args.get('filename') or request.form.get('filename')
        image_data_b64 = request.args.get('image_data') or request.form.get('image_data')

        # Validate inputs
        if not filename or not image_data_b64:
            return jsonify({'error': 'Missing filename or image_data parameter'}), 400

        if not validate_filename(filename):
            return jsonify({'error': 'Invalid filename'}), 400

        # Decode base64 image data
        try:
            image_data = base64.b64decode(image_data_b64)
        except Exception:
            return jsonify({'error': 'Invalid base64 encoding'}), 400

        # Validate that it's actually an image
        if not validate_image_bytes(image_data):
            return jsonify({'error': 'Invalid image data'}), 400

        # Create output directory if it doesn't exist
        output_dir = pathlib.Path('../assets/img').resolve()
        output_dir.mkdir(parents=True, exist_ok=True)

        # Construct file path with .png extension
        file_path = output_dir / f'{filename}.png'

        # Write the image file
        with open(file_path, 'wb') as f:
            f.write(image_data)

        return jsonify({'status': 'success', 'path': str(file_path)}), 200

    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
