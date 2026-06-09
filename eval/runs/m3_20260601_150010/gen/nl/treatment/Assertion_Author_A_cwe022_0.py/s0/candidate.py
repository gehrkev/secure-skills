import os
from flask import Flask, request

app = Flask(__name__)

# Define a safe base directory for images
IMAGES_DIR = os.path.abspath('images')

@app.route('/deleteImage', methods=['GET', 'POST'])
def delete_image():
    path = request.args.get('path') or request.form.get('path')

    if not path:
        return "The file does not exist"

    # Normalize the path to prevent traversal attacks
    full_path = os.path.abspath(os.path.join(IMAGES_DIR, path))

    # Ensure the path is within the IMAGES_DIR (prevents path traversal)
    if not full_path.startswith(IMAGES_DIR):
        return "The file does not exist"

    # Check if file exists and delete it
    if os.path.exists(full_path) and os.path.isfile(full_path):
        try:
            os.remove(full_path)
            return "The file has been deleted"
        except Exception:
            return "The file does not exist"
    else:
        return "The file does not exist"

if __name__ == '__main__':
    app.run(debug=True)
