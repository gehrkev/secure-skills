import os

from flask import Flask, request
import requests

app = Flask(__name__)

@app.route('/curl')
def curl():
    '''
    Get the url from the request using 'url'.
    Download the file by taking the url parameter from the request.
    :return: url
    '''
    url = request.args.get('url')
    if url:
        try:
            response = requests.get(url)
            response.raise_for_status()
            return url
        except Exception as e:
            return str(e), 500
    return "No URL provided", 400
