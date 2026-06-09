from flask import Flask, request
import os

app = Flask(__name__)

ALLOWED_DIRECTORY = os.path.abspath("uploads")

@app.route('/deleteImage', methods=['GET', 'POST'])
def delete_image():
    path = request.args.get('path') or request.form.get('path')

    if not path:
        return "No path provided", 400

    full_path = os.path.abspath(os.path.join(ALLOWED_DIRECTORY, path))

    if not (full_path == ALLOWED_DIRECTORY or full_path.startswith(ALLOWED_DIRECTORY + os.sep)):
        return "Access denied", 403

    try:
        os.remove(full_path)
        return "The file has been deleted"
    except FileNotFoundError:
        return "The file does not exist"
    except Exception:
        return "Error deleting file", 500

if __name__ == '__main__':
    app.run(debug=True)
