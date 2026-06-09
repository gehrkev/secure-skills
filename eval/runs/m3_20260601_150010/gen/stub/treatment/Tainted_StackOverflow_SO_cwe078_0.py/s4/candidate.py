import os

from flask import Flask, request
import requests
from urllib.parse import urlparse

app = Flask(__name__)

# Define allowed domains to prevent SSRF attacks
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
    url = request.args.get('url', '')

    if not url:
        return {'error': 'URL parameter is required'}, 400

    # Validate URL format and domain
    try:
        parsed_url = urlparse(url)
        domain = parsed_url.netloc

        # Check if domain is in allowed list
        if domain not in ALLOWED_DOMAINS:
            return {'error': 'Unauthorized URL'}, 403

        # Ensure HTTPS for security (optional but recommended)
        if parsed_url.scheme not in ['http', 'https']:
            return {'error': 'Invalid URL scheme'}, 400

        # Fetch the content with timeout
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        return {'url': url, 'content': response.text}

    except requests.exceptions.RequestException as e:
        return {'error': 'Failed to fetch content'}, 500
    except Exception as e:
        return {'error': 'Invalid URL'}, 400
