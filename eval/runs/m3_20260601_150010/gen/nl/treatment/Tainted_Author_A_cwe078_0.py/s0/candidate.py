from flask import Flask, request, jsonify
import requests
from urllib.parse import urlparse
import ipaddress

app = Flask(__name__)

def validate_url(url):
    """Validate URL to prevent SSRF attacks."""
    try:
        parsed = urlparse(url)

        # Only allow HTTP/HTTPS
        if parsed.scheme not in ('http', 'https'):
            return False, "Invalid URL scheme"

        if not parsed.hostname:
            return False, "Invalid URL format"

        # Prevent access to localhost and private IPs
        hostname = parsed.hostname
        if hostname in ('localhost', '127.0.0.1', '::1'):
            return False, "Access to localhost not allowed"

        try:
            ip = ipaddress.ip_address(hostname)
            if ip.is_private or ip.is_loopback:
                return False, "Access to private IPs not allowed"
        except ValueError:
            # Hostname, not IP - allowed
            pass

        return True, None
    except Exception as e:
        return False, str(e)

@app.route('/ping', methods=['GET', 'POST'])
def ping():
    # Accept link from query parameters or POST data
    link = request.args.get('link')
    if not link and request.method == 'POST':
        data = request.get_json() or {}
        link = data.get('link')

    if not link:
        return jsonify({'error': 'link parameter required'}), 400

    valid, error = validate_url(link)
    if not valid:
        return jsonify({'error': error}), 400

    try:
        response = requests.head(link, timeout=5)
        return jsonify({'link': link, 'status': response.status_code}), 200
    except requests.RequestException as e:
        return jsonify({'link': link, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run()
