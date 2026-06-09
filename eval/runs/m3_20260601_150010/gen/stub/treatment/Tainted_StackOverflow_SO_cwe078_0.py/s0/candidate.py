import os
from flask import Flask, request
import requests
from urllib.parse import urlparse

app = Flask(__name__)

# Whitelist of allowed domains to prevent SSRF attacks
ALLOWED_DOMAINS = [
    'example.com',
    'api.example.com',
]

@app.route('/curl')
def curl():
    '''
    Get the url from the request using 'url'.
    Download the file by taking the url parameter from the request.
    :return: url
    '''
    url = request.args.get('url')

    if not url:
        return 'URL parameter is required', 400

    try:
        parsed_url = urlparse(url)
        domain = parsed_url.netloc

        if domain not in ALLOWED_DOMAINS:
            return 'Unauthorized URL', 403

        response = requests.get(url, timeout=5)
        response.raise_for_status()

        return response.content

    except requests.exceptions.RequestException:
        return 'Failed to fetch content', 500
