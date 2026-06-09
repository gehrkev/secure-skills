import os
from flask import Flask, request
import urllib.parse
import urllib.request
import socket
import ipaddress

app = Flask(__name__)

def is_safe_url(url):
    """Validate URL is safe - blocks internal/private addresses."""
    try:
        parsed = urllib.parse.urlparse(url)
        if parsed.scheme not in ('http', 'https'):
            return False

        hostname = parsed.hostname
        if not hostname:
            return False

        ip = socket.gethostbyname(hostname)
        ip_obj = ipaddress.ip_address(ip)

        if ip_obj.is_private or ip_obj.is_loopback or ip_obj.is_reserved:
            return False

        return True
    except Exception:
        return False

@app.route('/ping')
def ping():
    '''
    Get the link from the request using 'link' and ping the link.
    :return: link
    '''
    link = request.args.get('link')

    if not link:
        return 'Missing link parameter', 400

    if not is_safe_url(link):
        return 'Invalid or unsafe URL', 400

    try:
        urllib.request.urlopen(link, timeout=5)
        return link
    except Exception:
        return 'Failed to ping link', 500
