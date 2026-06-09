from flask import Flask, request, send_from_directory
import os

app = Flask(__name__)

@app.route('/download', methods=['GET'])
def download():
    filename = request.args.get('filename')

    if not filename:
        return "Filename parameter is required", 400

    # Remove any directory components to prevent path traversal attacks
    filename = os.path.basename(filename)

    # Check if file exists in static directory
    file_path = os.path.join('static', filename)
    if not os.path.isfile(file_path):
        return "File not found", 404

    return send_from_directory('static', filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
