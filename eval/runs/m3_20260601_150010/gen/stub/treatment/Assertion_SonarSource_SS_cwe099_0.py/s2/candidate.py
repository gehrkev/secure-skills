from flask import request, send_file, Flask
from pathlib import Path

app = Flask(__name__)

@app.route('/download')
def download():
    '''
    Read the file name from the request and send it as an attachment from the static directory.
    '''
    filename = request.args.get('filename')

    if not filename:
        return 'Filename parameter required', 400

    # Prevent path traversal attacks
    if '..' in filename or filename.startswith('/'):
        return 'Invalid filename', 400

    # Get the safe path within static directory
    static_dir = Path(__file__).parent / 'static'
    file_path = static_dir / filename

    # Verify the file is within the static directory
    try:
        file_path = file_path.resolve()
        static_dir = static_dir.resolve()
        file_path.relative_to(static_dir)
    except (ValueError, RuntimeError):
        return 'Invalid filename', 400

    # Check if file exists
    if not file_path.is_file():
        return 'File not found', 404

    return send_file(str(file_path), as_attachment=True)
