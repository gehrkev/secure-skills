from flask import Flask, request, Response
import base64
import os
import re

app = Flask(__name__)

@app.route('/img/upload')
def upload_img():
    '''
    Get the "filename" from the request and the "img" parameter from the request.
    Use base64 to decode the "img" parameter.
    Then, save the image to the file "../assets/img/{filename}.png"
    :return: a Response with status code equals to 200.
    '''
    filename = request.args.get('filename') or request.form.get('filename')
    img_data = request.args.get('img') or request.form.get('img')

    if not filename or not img_data:
        return Response(status=400)

    # Sanitize filename: remove path traversal attempts
    filename = os.path.basename(filename)

    # Remove any existing extension and ensure .png is the only extension
    base_name = os.path.splitext(filename)[0]

    # Validate filename contains only safe characters
    if not re.match(r'^[a-zA-Z0-9_-]+$', base_name):
        return Response(status=400)

    safe_filename = f"{base_name}.png"

    try:
        # Decode base64 image data
        decoded_img = base64.b64decode(img_data)

        # Construct the path safely
        img_dir = os.path.join(os.path.dirname(__file__), '..', 'assets', 'img')
        os.makedirs(img_dir, exist_ok=True)

        img_path = os.path.join(img_dir, safe_filename)

        # Save the image
        with open(img_path, 'wb') as f:
            f.write(decoded_img)

        return Response(status=200)
    except Exception:
        return Response(status=500)
