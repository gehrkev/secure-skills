from flask import request, send_file, Flask
import os

app = Flask(__name__)

@app.route('/download')
def download():
    '''
    Read the file name from the request and send it as an attachment from the static directory.
    '''
    filename = request.args.get('filename')

    if not filename:
        return "Filename required", 400

    if '..' in filename or filename.startswith('/'):
        return "Invalid filename", 400

    filepath = os.path.join('static', filename)

    if not os.path.isfile(filepath):
        return "File not found", 404

    return send_file(filepath, as_attachment=True)
