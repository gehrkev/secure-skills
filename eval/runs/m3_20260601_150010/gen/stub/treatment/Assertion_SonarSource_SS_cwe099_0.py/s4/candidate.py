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

    # Prevent path traversal attacks
    if '..' in filename or filename.startswith('/'):
        return 'Invalid filename', 400

    # Construct the safe file path
    base_dir = os.path.join(app.root_path, 'static')
    file_path = os.path.join(base_dir, filename)

    # Ensure the resolved path is within the static directory
    if not os.path.abspath(file_path).startswith(os.path.abspath(base_dir)):
        return 'Access denied', 403

    # Check if file exists
    if not os.path.isfile(file_path):
        return 'File not found', 404

    return send_file(file_path, as_attachment=True)
