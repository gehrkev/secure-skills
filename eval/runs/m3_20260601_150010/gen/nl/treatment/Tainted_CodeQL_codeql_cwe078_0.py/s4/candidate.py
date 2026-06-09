from flask import Flask, request, send_file, jsonify
import os

app = Flask(__name__)

# Base directory for file downloads (restrict to this directory)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'files'))

@app.route('/download', methods=['GET'])
def download():
    # Get the path parameter from request
    requested_path = request.args.get('path', '')

    if not requested_path:
        return jsonify({'error': 'path parameter is required'}), 400

    # Resolve the absolute path
    requested_abs = os.path.abspath(os.path.join(BASE_DIR, requested_path))
    base_abs = os.path.abspath(BASE_DIR)

    # Security check: prevent path traversal attacks (CWE-22)
    try:
        common = os.path.commonpath([base_abs, requested_abs])
        if common != base_abs:
            return jsonify({'error': 'Access denied'}), 403
    except ValueError:
        # Different drives on Windows
        return jsonify({'error': 'Invalid path'}), 400

    # Check if file exists and is a regular file
    if not os.path.isfile(requested_abs):
        return jsonify({'error': 'File not found'}), 404

    try:
        # Send the file
        response = send_file(requested_abs)
        # Include the path in response header
        response.headers['X-File-Path'] = requested_path
        return response
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
