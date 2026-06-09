import base64
import os
from flask import Flask, request

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_image():
    filename = request.args.get('filename')
    image_data = request.args.get('image_data')

    if not filename or not image_data:
        return '', 400

    try:
        decoded_image = base64.b64decode(image_data)

        save_dir = '../assets/img'
        os.makedirs(save_dir, exist_ok=True)

        save_path = os.path.join(save_dir, f'{filename}.png')
        with open(save_path, 'wb') as f:
            f.write(decoded_image)

        return '', 200
    except Exception:
        return '', 500

if __name__ == '__main__':
    app.run()
