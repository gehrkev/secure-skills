from flask import Flask, request, Response
import base64
import os

app = Flask(__name__)

@app.route('/img/upload', methods=['GET', 'POST'])
def upload_img():
    '''
    Get the "filename" from the request and the "img" parameter from the request.
    Use base64 to decode the "img" parameter.
    Then, save the image to the file "../assets/img/{filename}.png"
    :return: a Response with status code equals to 200.
    '''
    filename = request.args.get('filename') or request.form.get('filename')
    img = request.args.get('img') or request.form.get('img')

    decoded_img = base64.b64decode(img)

    filepath = f'../assets/img/{filename}.png'
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    with open(filepath, 'wb') as f:
        f.write(decoded_img)

    return Response(status=200)
