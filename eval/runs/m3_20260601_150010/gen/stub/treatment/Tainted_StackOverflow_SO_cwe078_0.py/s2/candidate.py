import os
import urllib.request
from urllib.parse import urlparse

from flask import Flask, request

app = Flask(__name__)

# Define allowed URLs (or domains)
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
    # Get the user-provided URL
    url = request.args.get('url', '')

    # Validate URL is not empty
    if not url:
        return {'error': 'URL parameter is required'}, 400

    # Parse the URL to extract domain
    try:
        parsed_url = urlparse(url)
        domain = parsed_url.netloc
    except Exception:
        return {'error': 'Invalid URL format'}, 400

    # Validate against allowed domains
    if domain not in ALLOWED_DOMAINS:
        return {'error': 'Unauthorized URL'}, 400

    # Ensure the URL uses HTTPS or HTTP
    if parsed_url.scheme not in ('http', 'https'):
        return {'error': 'Invalid URL scheme'}, 400

    # Fetch content safely
    try:
        with urllib.request.urlopen(url, timeout=5) as response:
            content = response.read().decode('utf-8')
        return {'url': url, 'content': content}, 200
    except Exception as e:
        return {'error': 'Failed to fetch content'}, 500
