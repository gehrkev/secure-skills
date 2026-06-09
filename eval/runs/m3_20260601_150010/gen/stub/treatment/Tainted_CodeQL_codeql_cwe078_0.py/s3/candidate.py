import os
from flask import Flask, request, send_file, abort

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
        abort(400)

    filename = os.path.basename(path)
    safe_dir = os.path.abspath('./files')
    file_path = os.path.abspath(os.path.join(safe_dir, filename))

    if not file_path.startswith(safe_dir):
        abort(403)

    if not os.path.exists(file_path):
        abort(404)

    return send_file(file_path)
