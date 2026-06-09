import os
from flask import Flask, request, send_file

app = Flask(__name__)

FILE_MAPPING = {
    '1': 'file1.txt',
    '2': 'file2.txt',
    '3': 'file3.txt',
}

@app.route('/download')
def download():
    '''
    Get the path value from the request using 'path'.
    Download the file by taking the path parameter from the request.
    :return: path
    '''
    path_id = request.args.get('path')

    if path_id not in FILE_MAPPING:
        return {'error': 'Invalid path'}, 400

    file_path = FILE_MAPPING[path_id]

    if not os.path.exists(file_path):
        return {'error': 'File not found'}, 404

    return send_file(file_path)
