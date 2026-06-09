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

    # Prevent path traversal attacks
    base_dir = os.path.abspath('.')
    full_path = os.path.abspath(path)

    # Check if path is within base directory
    if not (full_path == base_dir or full_path.startswith(base_dir + os.sep)):
        return "The file does not exist"

    # Check if file exists and delete it
    if os.path.isfile(full_path):
        try:
            os.remove(full_path)
            return "The file has been deleted"
        except (OSError, IOError):
            return "The file does not exist"

    return "The file does not exist"
