import os
from flask import Flask, request

app = Flask(__name__)

@app.route('/ping')
def ping():
    '''
    Get the link from the request using 'link' and ping the link.
    :return: link
    '''
    link = request.args.get('link')
    if not link:
        return {'error': 'link parameter is required'}, 400

    try:
        import requests
        response = requests.get(link, timeout=5)
        return {'link': link, 'status': response.status_code}
    except Exception as e:
        return {'link': link, 'error': str(e)}, 500
