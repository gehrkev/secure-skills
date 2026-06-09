from flask import Flask, request, send_from_directory
import os

app = Flask(__name__)

STATIC_DIR = os.path.join(os.path.dirname(__file__), 'static')

@app.route('/download')
def download():
    filename = request.args.get('filename')

    if not filename:
        return "No filename provided", 400

    # Validate file path to prevent directory traversal (CWE-22)
    file_path = os.path.abspath(os.path.join(STATIC_DIR, filename))
    static_abs = os.path.abspath(STATIC_DIR)

    # Ensure the resolved path stays within the static directory
    if not file_path.startswith(static_abs + os.sep):
        return "Access denied", 403

    # Verify the file exists
    if not os.path.isfile(file_path):
        return "File not found", 404

    # Send the file as a download attachment
    return send_from_directory(STATIC_DIR, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
