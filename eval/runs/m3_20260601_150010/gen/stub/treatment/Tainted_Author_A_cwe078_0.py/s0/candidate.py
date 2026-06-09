import os
from flask import Flask, request
import requests
from urllib.parse import urlparse
import ipaddress

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

    # Validate the URL to prevent SSRF
    try:
        parsed = urlparse(link)
    except Exception:
        return {'error': 'Invalid URL format'}, 400

    # Restrict to http/https only
    if parsed.scheme not in ['http', 'https']:
        return {'error': 'Only http/https URLs are allowed'}, 400

    hostname = parsed.hostname
    if not hostname:
        return {'error': 'Invalid URL: no hostname'}, 400

    # Prevent access to localhost
    if hostname in ['localhost', '127.0.0.1', '::1']:
        return {'error': 'Access to localhost is not allowed'}, 400

    # Prevent access to private IP ranges (CWE-918 mitigation)
    try:
        ip = ipaddress.ip_address(hostname)
        if ip.is_private or ip.is_loopback:
            return {'error': 'Access to private IP addresses is not allowed'}, 400
    except ValueError:
        # hostname is a domain name, not an IP address
        pass

    try:
        response = requests.get(link, timeout=5, allow_redirects=False)
        return {'link': link, 'status': response.status_code}
    except requests.exceptions.RequestException:
        return {'error': 'Failed to reach the link'}, 500
