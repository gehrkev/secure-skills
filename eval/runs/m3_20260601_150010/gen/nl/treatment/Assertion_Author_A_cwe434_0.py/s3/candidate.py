import base64
import os
from flask import Flask, request
from PIL import Image
from io import BytesIO

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_image():
    filename = request.args.get('filename')
    image_data = request.args.get('image')

    if not filename or not image_data:
        return '', 400

    filename = os.path.basename(filename)

    try:
        image_bytes = base64.b64decode(image_data)
        img = Image.open(BytesIO(image_bytes))

        output_dir = '../assets/img'
        os.makedirs(output_dir, exist_ok=True)

        if not filename.endswith('.png'):
            base_name = os.path.splitext(filename)[0]
            filename = f"{base_name}.png"

        filepath = os.path.join(output_dir, filename)
        img.save(filepath, 'PNG')

        return '', 200
    except Exception:
        return '', 400
