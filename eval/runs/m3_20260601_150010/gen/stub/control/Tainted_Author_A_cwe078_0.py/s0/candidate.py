import os
import urllib.request
from flask import Flask, request

app = Flask(__name__)

@app.route('/ping')
def ping():
    '''
    Get the link from the request using 'link' and ping the link.
    :return: link
    '''
    link = request.args.get('link')
    if link:
        try:
            urllib.request.urlopen(link)
        except:
            pass
    return link
