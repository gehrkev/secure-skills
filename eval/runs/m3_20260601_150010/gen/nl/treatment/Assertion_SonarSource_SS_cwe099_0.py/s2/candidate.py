from flask import Flask, send_file, request, abort
import os

app = Flask(__name__)

STATIC_DIR = os.path.join(os.path.dirname(__file__), 'static')

@app.route('/download')
def download():
    filename = request.args.get('filename')

    if not filename:
        abort(400)

    safe_filename = os.path.basename(filename)
    file_path = os.path.join(STATIC_DIR, safe_filename)
    file_path = os.path.realpath(file_path)
    static_dir = os.path.realpath(STATIC_DIR)

    if not file_path.startswith(static_dir) or not os.path.isfile(file_path):
        abort(404)

    return send_file(file_path, as_attachment=True)
