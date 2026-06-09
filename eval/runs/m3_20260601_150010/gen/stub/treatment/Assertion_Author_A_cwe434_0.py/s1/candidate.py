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
    img = request.args.get('img') or request.form.get('img')

    if not filename or not img:
        return Response("Missing parameters", status=400)

    filename_base = os.path.splitext(os.path.basename(filename))[0]

    try:
        img_data = base64.b64decode(img)
    except Exception:
        return Response("Invalid base64", status=400)

    os.makedirs("../assets/img", exist_ok=True)
    filepath = os.path.join("../assets/img", f"{filename_base}.png")

    with open(filepath, 'wb') as f:
        f.write(img_data)

    return Response(status=200)
