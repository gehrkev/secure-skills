import base64
import os
from pathlib import Path
from flask import Flask, request
import re

app = Flask(__name__)

def is_valid_filename(filename):
    """Validate filename to prevent path traversal and ensure safe naming."""
    if not filename:
        return False
    # Reject path traversal attempts
    if '..' in filename or '/' in filename or '\\' in filename:
        return False
    # Ensure single extension (.png only)
    if not re.match(r'^[a-zA-Z0-9_\-]+\.png$', filename):
        return False
    return True

@app.route('/upload', methods=['POST'])
def upload_image():
    """Accept base64-encoded image data and save it."""
    try:
        filename = request.args.get('filename')
        image_data = request.args.get('image_data')

        if not filename or not image_data:
            return '', 400

        # Validate filename for security
        if not is_valid_filename(filename):
            return '', 400

        # Decode base64 data
        try:
            decoded_data = base64.b64decode(image_data, validate=True)
        except Exception:
            return '', 400

        # Create output directory if it doesn't exist
        output_dir = Path(__file__).parent.parent / 'assets' / 'img'
        output_dir.mkdir(parents=True, exist_ok=True)

        # Save the image
        output_path = output_dir / filename
        with open(output_path, 'wb') as f:
            f.write(decoded_data)

        return '', 200
    except Exception:
        return '', 500

if __name__ == '__main__':
    app.run(debug=False)
