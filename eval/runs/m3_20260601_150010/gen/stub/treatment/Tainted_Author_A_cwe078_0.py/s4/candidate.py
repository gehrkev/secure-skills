import os
from flask import Flask, request
import requests
from urllib.parse import urlparse

app = Flask(__name__)

# Whitelist of allowed domains for SSRF prevention
ALLOWED_DOMAINS = [
    'example.com',
    'api.example.com',
]

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
        parsed_url = urlparse(link)
        domain = parsed_url.netloc

        # Validate against whitelist to prevent SSRF
        if not any(domain.endswith(allowed) for allowed in ALLOWED_DOMAINS):
            return {'error': 'Domain not allowed'}, 403

        # Validate URL scheme
        if parsed_url.scheme not in ['http', 'https']:
            return {'error': 'Invalid URL scheme'}, 400

        # Attempt to ping the URL
        response = requests.head(link, timeout=5, allow_redirects=False)

        return {'link': link, 'status': response.status_code}
    except requests.RequestException as e:
        return {'error': 'Failed to ping'}, 500
    except Exception as e:
        return {'error': 'Invalid URL'}, 400
