from flask import Flask, request, jsonify
import requests
from urllib.parse import urlparse

app = Flask(__name__)

ALLOWED_DOMAINS = [
    'example.com',
    'api.example.com',
]

def is_url_allowed(url):
    """Validate URL against whitelist to prevent SSRF"""
    try:
        parsed = urlparse(url)
        if parsed.scheme not in ('http', 'https'):
            return False
        domain = parsed.netloc.lower()
        return any(domain.endswith(allowed) or domain == allowed for allowed in ALLOWED_DOMAINS)
    except Exception:
        return False

@app.route('/curl', methods=['GET'])
def curl():
    url = request.args.get('url')

    if not url:
        return jsonify({'error': 'url parameter is required'}), 400

    if not is_url_allowed(url):
        return jsonify({'error': 'URL not in whitelist'}), 400

    try:
        response = requests.get(url, timeout=10, allow_redirects=True)
        response.raise_for_status()
        return jsonify({'url': url, 'status': 'success'})
    except requests.RequestException as e:
        return jsonify({'error': f'Failed to fetch URL: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=False)
