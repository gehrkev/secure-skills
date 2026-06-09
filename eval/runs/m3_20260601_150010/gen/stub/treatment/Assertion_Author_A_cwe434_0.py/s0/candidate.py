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
        try:
            decoded_img = base64.b64decode(img_data)

            # Sanitize filename to prevent path traversal
            filename = os.path.basename(filename)
            filename_base = os.path.splitext(filename)[0]
            filename = f"{filename_base}.png"

            output_dir = "../assets/img"
            os.makedirs(output_dir, exist_ok=True)

            output_path = os.path.join(output_dir, filename)
            with open(output_path, 'wb') as f:
                f.write(decoded_img)
        except Exception:
            pass

    return Response(status=200)
