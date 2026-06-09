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

    if path is None:
        return "The file does not exist"

    base_dir = os.path.abspath(os.getcwd())
    full_path = os.path.abspath(os.path.join(base_dir, path))

    try:
        rel_path = os.path.relpath(full_path, base_dir)
        if rel_path.startswith('..'):
            return "The file does not exist"
    except ValueError:
        return "The file does not exist"

    if os.path.exists(full_path) and os.path.isfile(full_path):
        os.remove(full_path)
        return "The file has been deleted"
    else:
        return "The file does not exist"
