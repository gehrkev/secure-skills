from flask import Flask, request, Response
import base64
import os

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

    if filename and img_data:
        # Validate filename to prevent path traversal and multiple extensions
        if all(c.isalnum() or c in '_-' for c in filename):
            try:
                # Decode base64 image data
                decoded_img = base64.b64decode(img_data)

                # Create directory if it doesn't exist
                dir_path = "../assets/img"
                os.makedirs(dir_path, exist_ok=True)

                # Save the image
                file_path = os.path.join(dir_path, f"{filename}.png")
                with open(file_path, 'wb') as f:
                    f.write(decoded_img)
            except Exception:
                pass

    return Response(status=200)
