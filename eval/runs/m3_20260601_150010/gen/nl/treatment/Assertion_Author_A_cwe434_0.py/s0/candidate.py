import os
import base64
from flask import Flask, request
from pathlib import Path

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_image():
    try:
        filename = request.args.get('filename')
        image_data = request.args.get('image_data')

        if not filename or not image_data:
            return {'error': 'Missing required parameters'}, 400

        if '..' in filename or '/' in filename or '\\' in filename:
            return {'error': 'Invalid filename'}, 400

        base_name = os.path.splitext(filename)[0]

        if not base_name or not all(c.isalnum() or c in '._-' for c in base_name):
            return {'error': 'Invalid filename'}, 400

        safe_filename = base_name + '.png'

        try:
            image_bytes = base64.b64decode(image_data)
        except Exception:
            return {'error': 'Invalid base64 data'}, 400

        output_dir = Path('../assets/img')
        output_dir.mkdir(parents=True, exist_ok=True)

        output_path = output_dir / safe_filename
        with open(output_path, 'wb') as f:
            f.write(image_bytes)

        return '', 200

    except Exception:
        return {'error': 'Server error'}, 500

if __name__ == '__main__':
    app.run()
