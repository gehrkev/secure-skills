import os
from flask import Flask, request
import urllib.parse
import urllib.request
from urllib.error import URLError
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
        return {'error': 'Missing link parameter'}, 400

    try:
        parsed = urllib.parse.urlparse(link)

        # Only allow http/https schemes
        if parsed.scheme not in ['http', 'https']:
            return {'error': 'Invalid or unauthorized URL'}, 400

        # Block private/local addresses to prevent SSRF
        hostname = parsed.hostname
        if hostname:
            if hostname in ['localhost', '127.0.0.1', '0.0.0.0', '::1']:
                return {'error': 'Invalid or unauthorized URL'}, 400

            try:
                ip = ipaddress.ip_address(hostname)
                if ip.is_private or ip.is_loopback:
                    return {'error': 'Invalid or unauthorized URL'}, 400
            except ValueError:
                pass
    except Exception:
        return {'error': 'Invalid URL format'}, 400

    # Ping the link
    try:
        response = urllib.request.urlopen(link, timeout=5)
        return {'link': link}
    except URLError:
        return {'error': 'Failed to ping link'}, 500
