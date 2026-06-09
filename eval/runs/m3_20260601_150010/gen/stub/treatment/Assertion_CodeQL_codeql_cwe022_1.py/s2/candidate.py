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
    if '..' in file_name:
        return None

    if os.path.isabs(file_name):
        return None

    try:
        # Try to open the file from the current directory
        file_obj = open(file_name, 'r')

        # Verify the actual path is within the current directory
        real_file_path = os.path.realpath(file_obj.name)
        current_dir = os.path.realpath('.')

        if not real_file_path.startswith(current_dir + os.sep):
            file_obj.close()
            return None

        return file_obj
    except (IOError, OSError):
        return None
