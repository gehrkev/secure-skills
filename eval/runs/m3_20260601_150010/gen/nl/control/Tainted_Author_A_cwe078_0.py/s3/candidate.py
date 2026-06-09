from flask import Flask, request
import requests

app = Flask(__name__)

@app.route('/ping', methods=['GET'])
def ping():
    link = request.args.get('link')
    try:
        response = requests.head(link, timeout=5)
        return {'link': link, 'status': response.status_code}
    except Exception as e:
        return {'link': link, 'error': str(e)}

if __name__ == '__main__':
    app.run()
