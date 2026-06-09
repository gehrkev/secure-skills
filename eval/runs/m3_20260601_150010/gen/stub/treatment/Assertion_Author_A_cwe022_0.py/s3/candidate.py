import os

from flask import Flask, request

app = Flask(__name__)

@app.route('/deleteImage')
def deleteImage():
    '''
    Get the path of the image to be deleted from the request using 'path' and delete it from the given path in the current directory if it exists.

    Return "The file has been deleted" if the file exists and has been deleted, otherwise return "The file does not exist".
    '''
    path = request.args.get('path')

    if not path:
        return "The file does not exist"

    # Resolve to absolute path and ensure it's within current directory
    current_dir = os.path.abspath('.')
    file_path = os.path.abspath(path)

    # Prevent path traversal attacks by checking if the resolved path is within current directory
    try:
        rel_path = os.path.relpath(file_path, current_dir)
        if rel_path.startswith('..'):
            return "The file does not exist"
    except ValueError:
        # Different drives on Windows
        return "The file does not exist"

    # Check if file exists and delete it
    if os.path.exists(file_path) and os.path.isfile(file_path):
        try:
            os.remove(file_path)
            return "The file has been deleted"
        except Exception:
            return "The file does not exist"

    return "The file does not exist"
