from flask import Flask, request, jsonify
import requests
from urllib.parse import urlparse
import ipaddress

app = Flask(__name__)

# Whitelist of allowed domains
ALLOWED_DOMAINS = [
    'example.com',
    'api.example.com',
]

def is_private_ip(ip_str):
    """Check if an IP address is private/internal"""
    try:
        ip = ipaddress.ip_address(ip_str)
        return ip.is_private or ip.is_loopback
    except ValueError:
        return False

def is_allowed_url(url):
    """Validate URL to prevent SSRF attacks"""
    try:
        parsed = urlparse(url)

        # Ensure http or https scheme only
        if parsed.scheme not in ('http', 'https'):
            return False

        hostname = parsed.hostname
        if not hostname:
            return False

        # Check against whitelist
        if hostname not in ALLOWED_DOMAINS:
            return False

        return True
    except Exception:
        return False

@app.route('/curl', methods=['GET'])
def curl_endpoint():
    url = request.args.get('url')

    if not url:
        return jsonify({'error': 'Missing url parameter'}), 400

    if not is_allowed_url(url):
        return jsonify({'error': 'URL not allowed'}), 403

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        return response.content, response.status_code, {
            'Content-Type': response.headers.get('Content-Type', 'application/octet-stream')
        }
    except requests.exceptions.RequestException as e:
        return jsonify({'error': 'Failed to download file'}), 500

if __name__ == '__main__':
    app.run(debug=False)
