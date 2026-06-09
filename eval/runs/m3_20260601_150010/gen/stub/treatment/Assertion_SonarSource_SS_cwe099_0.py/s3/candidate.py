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
        return "Filename parameter missing", 400

    # Prevent path traversal by extracting only the filename
    filename = os.path.basename(filename)

    # Construct the file path within static directory
    file_path = os.path.join('static', filename)

    # Verify the file exists
    if not os.path.isfile(file_path):
        return "File not found", 404

    return send_file(file_path, as_attachment=True)
