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

    # Prevent path traversal attacks (CWE-22)
    current_dir = os.path.abspath(os.getcwd())
    target_path = os.path.abspath(os.path.join(current_dir, path))

    try:
        # Verify the target path is within the current directory
        rel_path = os.path.relpath(target_path, current_dir)
        if rel_path.startswith('..'):
            return "The file does not exist"
    except ValueError:
        # Different drives on Windows
        return "The file does not exist"

    # Delete the file if it exists
    if os.path.isfile(target_path):
        try:
            os.remove(target_path)
            return "The file has been deleted"
        except OSError:
            return "The file does not exist"

    return "The file does not exist"
