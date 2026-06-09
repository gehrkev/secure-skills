import os
from flask import Flask, request

app = Flask(__name__)

# Define a safe directory for file deletion operations
SAFE_DIRECTORY = os.path.abspath('./uploads')

@app.route('/deleteImage', methods=['GET', 'POST'])
def delete_image():
    # Get path parameter from request (query string or form data)
    path = request.args.get('path') or request.form.get('path')

    if not path:
        return "No path provided", 400

    # Normalize the path and resolve relative paths
    requested_path = os.path.abspath(path)

    # Validate path is within the safe directory (prevent path traversal attacks)
    if not requested_path.startswith(SAFE_DIRECTORY + os.sep) and requested_path != SAFE_DIRECTORY:
        return "Invalid path", 403

    try:
        if os.path.exists(requested_path):
            os.remove(requested_path)
            return "The file has been deleted"
        else:
            return "The file does not exist"
    except Exception as e:
        return f"Error deleting file: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=False)
