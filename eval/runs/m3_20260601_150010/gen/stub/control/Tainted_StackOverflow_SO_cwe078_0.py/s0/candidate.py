import os
import urllib.request

from flask import Flask, request

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
            with urllib.request.urlopen(url) as response:
                return response.read()
        except Exception as e:
            return str(e), 400
    return ""
