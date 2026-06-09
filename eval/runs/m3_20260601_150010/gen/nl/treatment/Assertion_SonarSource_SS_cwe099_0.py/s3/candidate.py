from flask import Flask, request, send_from_directory
import os

app = Flask(__name__)

@app.route('/download')
def download():
    filename = request.args.get('filename')

    if not filename:
        return 'Filename not provided', 400

    if '..' in filename or filename.startswith('/'):
        return 'Invalid filename', 400

    static_dir = os.path.join(os.path.dirname(__file__), 'static')

    try:
        return send_from_directory(static_dir, filename, as_attachment=True)
    except FileNotFoundError:
        return 'File not found', 404

if __name__ == '__main__':
    app.run()
