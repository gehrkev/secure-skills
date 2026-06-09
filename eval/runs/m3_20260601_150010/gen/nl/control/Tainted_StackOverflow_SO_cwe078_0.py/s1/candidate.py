from flask import Flask, request, send_file
import requests
from io import BytesIO

app = Flask(__name__)

@app.route('/curl', methods=['GET'])
def curl():
    url = request.args.get('url')
    if not url:
        return "URL parameter is required", 400

    try:
        response = requests.get(url)
        response.raise_for_status()
        file_obj = BytesIO(response.content)
        return send_file(file_obj, mimetype=response.headers.get('content-type', 'application/octet-stream'))
    except requests.RequestException as e:
        return str(e), 400

if __name__ == '__main__':
    app.run()
