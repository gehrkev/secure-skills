from flask import Flask, request, jsonify
import requests
from urllib.parse import urlparse

app = Flask(__name__)

def is_valid_url(url):
    """Validate URL to prevent SSRF attacks"""
    try:
        parsed = urlparse(url)

        if parsed.scheme not in ['http', 'https']:
            return False

        hostname = parsed.hostname
        if not hostname:
            return False

        if hostname in ['localhost', '127.0.0.1', '0.0.0.0', '::1']:
            return False

        if hostname.startswith('192.168.') or hostname.startswith('10.') or hostname.startswith('172.'):
            return False

        return True
    except:
        return False

@app.route('/ping', methods=['GET', 'POST'])
def ping():
    link = request.args.get('link') or (request.json.get('link') if request.is_json else None) or request.form.get('link')

    if not link:
        return jsonify({'error': 'link parameter is required'}), 400

    if not is_valid_url(link):
        return jsonify({'error': 'Invalid or unauthorized URL'}), 400

    try:
        response = requests.head(link, timeout=5, allow_redirects=True)
        return jsonify({'link': link, 'status_code': response.status_code}), 200
    except requests.exceptions.Timeout:
        return jsonify({'error': 'Request timeout'}), 504
    except requests.exceptions.ConnectionError:
        return jsonify({'error': 'Connection failed'}), 503
    except Exception as e:
        return jsonify({'error': 'Failed to ping link'}), 500

if __name__ == '__main__':
    app.run()
