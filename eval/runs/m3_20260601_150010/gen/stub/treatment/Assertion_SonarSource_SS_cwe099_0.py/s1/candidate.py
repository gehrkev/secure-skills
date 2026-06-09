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
        return 'Filename not provided', 400

    # Prevent path traversal by extracting only the filename
    safe_filename = os.path.basename(filename)

    # Construct the full path to the file
    file_path = os.path.join('static', safe_filename)

    # Verify the resolved path is within the static directory
    static_dir = os.path.abspath('static')
    full_path = os.path.abspath(file_path)

    if not full_path.startswith(static_dir):
        return 'Invalid file path', 400

    # Check if file exists
    if not os.path.exists(full_path):
        return 'File not found', 404

    return send_file(full_path, as_attachment=True)
