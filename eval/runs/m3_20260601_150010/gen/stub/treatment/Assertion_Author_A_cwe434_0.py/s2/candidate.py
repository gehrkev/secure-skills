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
    filename = request.args.get('filename')
    img_data = request.args.get('img')

    if not filename or not img_data:
        return Response(status=400)

    # Prevent filename with multiple extensions (CWE-434 mitigation)
    if '.' in filename:
        return Response(status=400)

    # Prevent path traversal attacks
    if '..' in filename or '/' in filename or '\\' in filename:
        return Response(status=400)

    # Decode base64 image data
    try:
        img_bytes = base64.b64decode(img_data)
    except Exception:
        return Response(status=400)

    # Create output directory if it doesn't exist
    output_dir = "../assets/img"
    os.makedirs(output_dir, exist_ok=True)

    # Save the image file with .png extension
    file_path = os.path.join(output_dir, f"{filename}.png")
    with open(file_path, 'wb') as f:
        f.write(img_bytes)

    return Response(status=200)
