from flask import Flask, request
import os

app = Flask(__name__)

@app.route('/open_file')
def open_file():
    filename = request.args.get('filename') or request.form.get('filename')

    if not filename:
        return None

    try:
        current_dir = os.getcwd()
        file_path = os.path.abspath(os.path.join(current_dir, filename))

        # Security check: prevent path traversal attacks
        rel_path = os.path.relpath(file_path, current_dir)
        if rel_path.startswith('..'):
            return None

        return open(file_path, 'rb')
    except (FileNotFoundError, IOError, OSError, ValueError):
        return None
