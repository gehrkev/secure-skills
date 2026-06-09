from flask import Flask, request, send_file
import os

app = Flask(__name__)

@app.route('/download')
def download():
    path = request.args.get('path')

    if not path or not os.path.exists(path):
        return {'error': 'Invalid or missing path'}, 400

    return send_file(path, as_attachment=True)

if __name__ == '__main__':
    app.run()
