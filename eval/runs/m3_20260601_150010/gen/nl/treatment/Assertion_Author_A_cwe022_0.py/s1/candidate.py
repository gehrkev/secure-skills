from flask import Flask, request
import os

app = Flask(__name__)

ALLOWED_DIRECTORY = os.path.abspath("./uploads")

@app.route('/deleteImage', methods=['GET', 'POST'])
def delete_image():
    path = request.args.get('path') or request.form.get('path')

    if not path:
        return "Path parameter required", 400

    full_path = os.path.abspath(path)

    # Prevent path traversal attacks by restricting to allowed directory
    try:
        relative = os.path.relpath(full_path, ALLOWED_DIRECTORY)
        if relative.startswith('..'):
            return "Access denied", 403
    except ValueError:
        return "Access denied", 403

    # Check if file exists and is a file
    if not os.path.isfile(full_path):
        return "The file does not exist"

    try:
        os.remove(full_path)
        return "The file has been deleted"
    except OSError:
        return "The file does not exist"

if __name__ == '__main__':
    app.run()
