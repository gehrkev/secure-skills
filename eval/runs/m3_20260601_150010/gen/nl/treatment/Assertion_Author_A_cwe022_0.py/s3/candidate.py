import flask
from pathlib import Path

app = flask.Flask(__name__)

# Safe base directory for file operations
SAFE_DIR = Path("./uploads")

@app.route('/deleteImage', methods=['GET', 'POST'])
def delete_image():
    path = flask.request.args.get('path') or flask.request.form.get('path')

    if not path:
        return "Invalid path", 400

    try:
        # Construct the full path and resolve it to prevent traversal
        target_path = (SAFE_DIR / path).resolve()
        safe_base = SAFE_DIR.resolve()

        # Verify the target path is within the safe directory
        target_path.relative_to(safe_base)
    except (ValueError, RuntimeError):
        # Path traversal attempt detected
        return "Invalid path", 403

    # Check if file exists and delete it
    try:
        if target_path.exists():
            target_path.unlink()
            return "The file has been deleted"
        else:
            return "The file does not exist"
    except Exception:
        return "Error deleting file", 500

if __name__ == '__main__':
    app.run(debug=True)
