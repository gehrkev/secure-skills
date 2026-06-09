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

    try:
        # Get the current directory and join with filename
        file_path = os.path.join(os.getcwd(), file_name)

        # Resolve to absolute path and normalize
        file_path = os.path.abspath(file_path)

        # Get the real path (follows symlinks)
        file_path = os.path.realpath(file_path)
        current_dir = os.path.realpath(os.getcwd())

        # Prevent path traversal by checking if the file is within current directory
        if not file_path.startswith(current_dir + os.sep):
            return None

        # Try to open the file
        return open(file_path, 'r')
    except (OSError, IOError):
        return None
