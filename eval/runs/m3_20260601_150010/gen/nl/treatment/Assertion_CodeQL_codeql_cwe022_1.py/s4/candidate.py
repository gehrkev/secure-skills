from flask import Flask, request
import os

app = Flask(__name__)

@app.route('/open_file')
def open_file():
    filename = request.args.get('filename')

    if not filename:
        return None

    # Get absolute path of the requested file
    file_path = os.path.abspath(filename)
    # Get absolute path of current directory
    current_dir = os.path.abspath('.')

    # Check that the file is within the current directory (prevent path traversal)
    if not file_path.startswith(current_dir + os.sep):
        return None

    try:
        # Open and return the file object
        return open(file_path, 'r')
    except:
        return None
