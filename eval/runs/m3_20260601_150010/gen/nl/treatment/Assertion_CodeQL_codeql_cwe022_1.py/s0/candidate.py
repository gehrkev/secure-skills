from flask import Flask, request
import os

app = Flask(__name__)

@app.route('/open_file', methods=['GET', 'POST'])
def open_file():
    filename = request.args.get('filename') or request.form.get('filename')

    if not filename:
        return None

    try:
        current_dir = os.path.abspath('.')
        file_path = os.path.abspath(filename)

        # Prevent path traversal: ensure file is within current directory
        if not (file_path == current_dir or file_path.startswith(current_dir + os.sep)):
            return None

        file_obj = open(file_path, 'rb')
        return file_obj
    except (OSError, IOError, TypeError):
        return None

if __name__ == '__main__':
    app.run()
