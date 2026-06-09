from flask import Flask, request, send_file, jsonify
import os

app = Flask(__name__)

# Define the allowed base directory for downloads
ALLOWED_DIR = os.path.abspath('/tmp/downloads')

@app.route('/download', methods=['GET'])
def download():
    # Get the path parameter from the request
    path = request.args.get('path', '')

    if not path:
        return jsonify({'error': 'path parameter is required'}), 400

    # Resolve the full path
    full_path = os.path.abspath(os.path.join(ALLOWED_DIR, path))

    # Prevent path traversal: ensure the resolved path is within ALLOWED_DIR
    if not full_path.startswith(ALLOWED_DIR + os.sep) and full_path != ALLOWED_DIR:
        return jsonify({'error': 'Unauthorized path access'}), 403

    # Check if the file exists and is a regular file
    if not os.path.exists(full_path) or not os.path.isfile(full_path):
        return jsonify({'error': 'File not found'}), 404

    try:
        # Send the file to the client and return the path
        return send_file(full_path, as_attachment=True)
    except Exception as e:
        return jsonify({'error': 'Failed to download file', 'details': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=False)
