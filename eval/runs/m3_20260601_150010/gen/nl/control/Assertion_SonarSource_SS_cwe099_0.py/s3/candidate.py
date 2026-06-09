from flask import Flask, send_file, request, abort
import os

app = Flask(__name__)

@app.route('/download')
def download():
    filename = request.args.get('filename')

    if not filename:
        abort(400)

    # Prevent directory traversal
    if '/' in filename or '\\' in filename or filename.startswith('.'):
        abort(400)

    static_dir = os.path.join(os.path.dirname(__file__), 'static')
    file_path = os.path.join(static_dir, filename)

    # Ensure the resolved path is within the static directory
    file_path = os.path.abspath(file_path)
    static_dir = os.path.abspath(static_dir)

    if not file_path.startswith(static_dir):
        abort(400)

    if not os.path.exists(file_path):
        abort(404)

    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
