from flask import Flask, request
import requests

app = Flask(__name__)

@app.route('/ping')
def ping():
    link = request.args.get('link')
    if not link:
        return {'error': 'link parameter required'}, 400

    try:
        response = requests.get(link)
        return {'status': response.status_code}
    except Exception as e:
        return {'error': str(e)}, 500

if __name__ == '__main__':
    app.run()
