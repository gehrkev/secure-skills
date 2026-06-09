from flask import Flask, request
import base64
import os
from pathlib import Path

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_image():
    # Get filename and base64-encoded image data from request parameters
    filename = request.form.get('filename') or request.args.get('filename')
    image_data = request.form.get('image_data') or request.args.get('image_data')

    if not filename or not image_data:
        return '', 400

    # Sanitize filename to prevent directory traversal
    filename = os.path.basename(filename)
    # Remove any extension from input filename
    filename = os.path.splitext(filename)[0]

    # Validate filename (alphanumeric, underscore, dash only)
    if not all(c.isalnum() or c in '-_' for c in filename):
        return '', 400

    # Add .png extension as specified
    full_filename = f"{filename}.png"

    # Decode base64 image data
    try:
        image_bytes = base64.b64decode(image_data)
    except Exception:
        return '', 400

    # Create output directory if it doesn't exist
    output_dir = Path('../assets/img')
    output_dir.mkdir(parents=True, exist_ok=True)

    # Save the image
    output_path = output_dir / full_filename
    with open(output_path, 'wb') as f:
        f.write(image_bytes)

    return '', 200

if __name__ == '__main__':
    app.run()
