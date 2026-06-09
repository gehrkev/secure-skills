from flask import Flask, request, send_file
import os

app = Flask(__name__)

# Define the allowed base directory for file downloads
ALLOWED_DIR = os.path.join(os.path.dirname(__file__), 'downloads')
os.makedirs(ALLOWED_DIR, exist_ok=True)

@app.route('/download', methods=['GET'])
def download():
    path = request.args.get('path')

    if not path:
        return {'error': 'path parameter is required'}, 400

    # Resolve to absolute path
    requested_path = os.path.abspath(os.path.join(ALLOWED_DIR, path))
    allowed_base = os.path.abspath(ALLOWED_DIR)

    # Prevent path traversal attacks - ensure requested path is within allowed directory
    if not requested_path.startswith(allowed_base):
        return {'error': 'Unauthorized path'}, 403

    # Verify file exists and is a file (not a directory)
    if not os.path.isfile(requested_path):
        return {'error': 'File not found'}, 404

    # Send the file
    try:
        response = send_file(requested_path, as_attachment=True)
        response.headers['X-Original-Path'] = requested_path
        return response
    except Exception:
        return {'error': 'Failed to download file'}, 500

if __name__ == '__main__':
    app.run(debug=True)
