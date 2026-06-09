from flask import Flask, request, send_file
import os

app = Flask(__name__)

@app.route('/download')
def download():
    path = request.args.get('path')

    if not path:
        return {'error': 'path parameter is required'}, 400

    if not os.path.exists(path):
        return {'error': 'File not found'}, 404

    try:
        return send_file(path, as_attachment=True)
    except Exception as e:
        return {'error': str(e)}, 500

if __name__ == '__main__':
    app.run(debug=True)
