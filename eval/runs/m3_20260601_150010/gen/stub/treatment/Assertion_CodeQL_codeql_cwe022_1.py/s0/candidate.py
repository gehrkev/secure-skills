from flask import Flask, request
import re
import os

app = Flask(__name__)



@app.route('/open_file')
def open_file():
    '''
    Get the file name from the request using 'file_name' and check if the file opens successfully in the given path from the current directory.

    :return: The file object if the file opens successfully, None otherwise.
    '''
    file_name = request.args.get('file_name')

    if not file_name:
        return None

    # Prevent path traversal attacks (CWE-22)
    if os.path.isabs(file_name):
        return None

    # Resolve the full path and ensure it's within the current directory
    current_dir = os.path.abspath(os.getcwd())
    target_path = os.path.abspath(os.path.join(current_dir, file_name))

    # Ensure the resolved path is within the current directory
    if not target_path.startswith(current_dir + os.sep):
        if target_path != current_dir:
            return None

    try:
        return open(target_path, 'r')
    except (IOError, OSError):
        return None
