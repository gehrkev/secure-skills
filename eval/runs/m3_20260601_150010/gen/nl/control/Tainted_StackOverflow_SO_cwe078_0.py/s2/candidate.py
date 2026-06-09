from flask import Flask, request
import urllib.request

app = Flask(__name__)

@app.route('/curl')
def curl():
    url = request.args.get('url')

    if not url:
        return {'error': 'url parameter is required'}, 400

    try:
        urllib.request.urlretrieve(url, 'downloaded_file')
        return {'url': url}, 200
    except Exception as e:
        return {'error': str(e)}, 400

if __name__ == '__main__':
    app.run()
