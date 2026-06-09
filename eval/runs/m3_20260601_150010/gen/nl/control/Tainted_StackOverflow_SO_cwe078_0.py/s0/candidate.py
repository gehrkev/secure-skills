from flask import Flask, request
import requests

app = Flask(__name__)

@app.route('/curl', methods=['GET'])
def curl():
    url = request.args.get('url')
    if not url:
        return {'error': 'url parameter is required'}, 400

    try:
        response = requests.get(url)
        response.raise_for_status()
        return {'url': url}
    except requests.RequestException as e:
        return {'error': str(e)}, 400

if __name__ == '__main__':
    app.run(debug=True)
