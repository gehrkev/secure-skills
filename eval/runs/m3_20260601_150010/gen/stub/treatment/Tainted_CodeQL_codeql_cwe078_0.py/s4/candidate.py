import os
from flask import Flask, request, send_file

app = Flask(__name__)

FILE_MAP = {
    'file1': '/safe/path/to/file1.txt',
    'file2': '/safe/path/to/file2.txt',
}

@app.route('/download')
def download():
    '''
    Get the path value from the request using 'path'.
    Download the file by taking the path parameter from the request.
    :return: path
    '''
    path = request.args.get('path')

    if path not in FILE_MAP:
        return 'File not found', 404

    safe_path = FILE_MAP[path]

    if os.path.exists(safe_path):
        return send_file(safe_path, as_attachment=True)
    else:
        return 'File not found', 404
