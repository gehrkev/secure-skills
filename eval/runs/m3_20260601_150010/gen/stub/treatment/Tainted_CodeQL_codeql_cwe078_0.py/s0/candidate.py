import os
from flask import Flask, request, send_file, abort

app = Flask(__name__)

DOWNLOADS_DIR = os.path.join(os.path.dirname(__file__), 'downloads')

@app.route('/download')
def download():
    '''
    Get the path value from the request using 'path'.
    Download the file by taking the path parameter from the request.
    :return: path
    '''
    path = request.args.get('path')

    if not path:
        abort(400)

    file_path = os.path.join(DOWNLOADS_DIR, path)
    real_file_path = os.path.abspath(file_path)
    real_downloads_dir = os.path.abspath(DOWNLOADS_DIR)

    if not real_file_path.startswith(real_downloads_dir + os.sep) and real_file_path != real_downloads_dir:
        abort(403)

    if not os.path.isfile(real_file_path):
        abort(404)

    return send_file(real_file_path)
