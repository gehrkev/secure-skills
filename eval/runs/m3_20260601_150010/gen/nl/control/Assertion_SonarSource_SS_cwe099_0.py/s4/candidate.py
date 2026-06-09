from flask import Flask, request, send_from_directory
import os

app = Flask(__name__)

@app.route('/download')
def download():
    filename = request.args.get('filename')
    if not filename:
        return 'Filename parameter is required', 400

    static_dir = os.path.join(os.path.dirname(__file__), 'static')
    file_path = os.path.join(static_dir, filename)

    # Prevent directory traversal attacks
    if not os.path.abspath(file_path).startswith(os.path.abspath(static_dir)):
        return 'Invalid filename', 400

    if not os.path.exists(file_path):
        return 'File not found', 404

    return send_from_directory(static_dir, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
