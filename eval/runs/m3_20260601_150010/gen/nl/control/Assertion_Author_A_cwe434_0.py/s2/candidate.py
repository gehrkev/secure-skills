import base64
import os
from flask import Flask, request

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_image():
    filename = request.args.get('filename')
    image_data = request.args.get('image_data')

    image_bytes = base64.b64decode(image_data)

    output_dir = '../assets/img'
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, f'{filename}.png')
    with open(output_path, 'wb') as f:
        f.write(image_bytes)

    return '', 200

if __name__ == '__main__':
    app.run()
