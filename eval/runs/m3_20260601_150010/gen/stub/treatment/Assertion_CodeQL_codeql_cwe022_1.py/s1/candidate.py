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

    # Prevent path traversal attacks
    if re.search(r'\.\.', file_name) or file_name.startswith('/'):
        return None

    try:
        file_obj = open(file_name, 'r')
        return file_obj
    except (FileNotFoundError, IOError, OSError):
        return None
