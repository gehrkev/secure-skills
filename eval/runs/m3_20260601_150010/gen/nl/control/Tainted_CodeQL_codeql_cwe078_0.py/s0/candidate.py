from flask import Flask, request, send_file
import os

app = Flask(__name__)

@app.route('/download', methods=['GET'])
def download():
    path = request.args.get('path')
    if not path:
        return {'error': 'path parameter is required'}, 400

    if os.path.exists(path):
        return send_file(path, as_attachment=True)
    else:
        return {'error': 'file not found'}, 404

if __name__ == '__main__':
    app.run()
