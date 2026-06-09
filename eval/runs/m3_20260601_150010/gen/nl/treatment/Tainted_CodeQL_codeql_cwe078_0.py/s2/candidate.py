from flask import Flask, request, send_file, jsonify
import os

app = Flask(__name__)

# Define allowed base directory for downloads
ALLOWED_BASE_DIR = os.path.join(os.getcwd(), 'downloads')

@app.route('/download', methods=['GET'])
def download():
    path = request.args.get('path', '')

    if not path:
        return jsonify({'error': 'path parameter is required'}), 400

    # Resolve the full path
    full_path = os.path.join(ALLOWED_BASE_DIR, path)

    # Normalize the path to prevent directory traversal
    real_path = os.path.realpath(full_path)
    allowed_base = os.path.realpath(ALLOWED_BASE_DIR)

    # Check if the resolved path is within the allowed directory
    if not real_path.startswith(allowed_base):
        return jsonify({'error': 'Access denied'}), 403

    # Check if the file exists
    if not os.path.isfile(real_path):
        return jsonify({'error': 'File not found'}), 404

    # Return the file
    return send_file(real_path)

if __name__ == '__main__':
    app.run(debug=False)
