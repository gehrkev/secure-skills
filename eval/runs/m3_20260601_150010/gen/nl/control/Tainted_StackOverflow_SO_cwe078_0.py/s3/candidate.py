from flask import Flask, request
import urllib.request

app = Flask(__name__)

@app.route('/curl')
def curl():
    url = request.args.get('url')
    if not url:
        return 'url parameter required', 400

    try:
        response = urllib.request.urlopen(url)
        return response.read()
    except Exception as e:
        return f'Error: {str(e)}', 500

if __name__ == '__main__':
    app.run()
