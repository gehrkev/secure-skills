from flask import Flask, request
import os

app = Flask(__name__)

@app.route('/open_file')
def open_file():
    filename = request.args.get('filename') or request.form.get('filename')

    if not filename:
        return None

    # Normalize the path to prevent path traversal
    filepath = os.path.normpath(os.path.join('.', filename))

    # Ensure the file stays within the current directory
    current_dir = os.path.abspath('.')
    absolute_filepath = os.path.abspath(filepath)

    if not absolute_filepath.startswith(current_dir + os.sep) and absolute_filepath != current_dir:
        return None

    try:
        return open(filepath, 'r')
    except (IOError, OSError):
        return None
