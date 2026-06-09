import os
from flask import Flask, request, send_file

app = Flask(__name__)

# Define the allowed base directory for downloads
ALLOWED_DIR = os.path.abspath('./files')

@app.route('/download', methods=['GET'])
def download():
    # Get the path parameter from the request
    path = request.args.get('path', '')

    if not path:
        return {'error': 'path parameter is required'}, 400

    # Construct the full file path
    full_path = os.path.abspath(os.path.join(ALLOWED_DIR, path))

    # Security check: ensure the resolved path is within ALLOWED_DIR
    try:
        if os.path.commonpath([ALLOWED_DIR, full_path]) != ALLOWED_DIR:
            return {'error': 'Invalid path'}, 403
    except ValueError:
        # commonpath raises ValueError if paths are on different drives (Windows)
        return {'error': 'Invalid path'}, 403

    # Verify the file exists and is a regular file
    if not os.path.isfile(full_path):
        return {'error': 'File not found'}, 404

    try:
        # Send the file as a download
        return send_file(full_path, as_attachment=True)
    except Exception as e:
        return {'error': 'Failed to download file'}, 500

if __name__ == '__main__':
    app.run(debug=True)
