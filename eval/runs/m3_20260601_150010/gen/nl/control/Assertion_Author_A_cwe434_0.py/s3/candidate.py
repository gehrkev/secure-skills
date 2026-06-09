from flask import Flask, request
import base64
import os

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_image():
    filename = request.args.get('filename') or request.form.get('filename')
    base64_data = request.args.get('image') or request.form.get('image')

    if not filename or not base64_data:
        return '', 400

    try:
        image_data = base64.b64decode(base64_data)

        os.makedirs('../assets/img', exist_ok=True)

        filepath = f'../assets/img/{filename}.png'
        with open(filepath, 'wb') as f:
            f.write(image_data)

        return '', 200
    except Exception:
        return '', 500

if __name__ == '__main__':
    app.run()
