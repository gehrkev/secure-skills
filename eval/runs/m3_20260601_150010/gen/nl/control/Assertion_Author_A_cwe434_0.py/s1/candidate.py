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
        decoded_data = base64.b64decode(image_data)

        output_dir = '../assets/img'
        os.makedirs(output_dir, exist_ok=True)

        output_path = os.path.join(output_dir, f'{filename}.png')
        with open(output_path, 'wb') as f:
            f.write(decoded_data)

        return '', 200
    except Exception as e:
        return '', 500

if __name__ == '__main__':
    app.run()
