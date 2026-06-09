from flask import Flask, request
import requests

app = Flask(__name__)

@app.route('/ping')
def ping():
    link = request.args.get('link')
    if not link:
        return {'error': 'link parameter is required'}, 400

    try:
        response = requests.head(link, timeout=5)
        return {'link': link, 'status_code': response.status_code}
    except Exception as e:
        return {'link': link, 'error': str(e)}, 500

if __name__ == '__main__':
    app.run()
