import os
from flask import Flask, request
import requests
from urllib.parse import urlparse

app = Flask(__name__)

@app.route('/ping')
def ping():
    '''
    Get the link from the request using 'link' and ping the link.
    :return: link
    '''
    link = request.args.get('link', '')

    if not link:
        return {'error': 'link parameter is required'}, 400

    try:
        # Validate URL to prevent SSRF attacks
        parsed = urlparse(link)

        # Only allow http and https schemes
        if parsed.scheme not in ('http', 'https'):
            return {'error': 'Invalid URL scheme'}, 400

        hostname = parsed.hostname
        if not hostname:
            return {'error': 'Invalid URL'}, 400

        # Block access to internal/private IP ranges
        private_ranges = [
            'localhost',
            '127.0.0.1',
            '0.0.0.0',
        ]

        if hostname in private_ranges or \
           hostname.startswith('192.168.') or \
           hostname.startswith('10.') or \
           hostname.startswith('172.'):
            return {'error': 'Access to internal resources not allowed'}, 403

        # Ping the link with a HEAD request
        response = requests.head(link, timeout=5, allow_redirects=False)

        # Return the link if reachable
        return {'link': link, 'status': response.status_code}

    except requests.RequestException:
        return {'error': 'Failed to reach the link'}, 500
    except Exception:
        return {'error': 'Invalid request'}, 400
