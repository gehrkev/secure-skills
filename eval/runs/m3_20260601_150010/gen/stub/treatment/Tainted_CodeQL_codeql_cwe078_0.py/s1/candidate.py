import os
from flask import Flask, request, send_file

app = Flask(__name__)

@app.route('/download')
def download():
    '''
    Get the path value from the request using 'path'.
    Download the file by taking the path parameter from the request.
    :return: path
    '''
    path = request.args.get('path')

    if not path:
        return {'error': 'path parameter required'}, 400

    base_dir = os.path.abspath('.')
    file_path = os.path.abspath(os.path.join(base_dir, path))

    if not file_path.startswith(base_dir):
        return {'error': 'Invalid path'}, 403

    if os.path.isfile(file_path):
        return send_file(file_path)

    return path
