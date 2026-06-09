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
        return 'Filename parameter required', 400

    # Get just the filename, removing any path components to prevent traversal
    filename = os.path.basename(filename)

    # Construct the full path
    filepath = os.path.join(app.static_folder, filename)

    # Verify the resolved path is within the static directory
    static_path = os.path.abspath(app.static_folder)
    resolved_path = os.path.abspath(filepath)

    if not resolved_path.startswith(static_path):
        return 'Invalid file path', 403

    # Check if file exists
    if not os.path.isfile(resolved_path):
        return 'File not found', 404

    return send_file(resolved_path, as_attachment=True)
