from flask import Flask, request, jsonify
import requests
from urllib.parse import urlparse

app = Flask(__name__)

# Define allowed domains to prevent SSRF attacks
ALLOWED_DOMAINS = [
    'example.com',
    'api.example.com',
]

def is_url_allowed(url):
    """Validate URL against allowed domains to prevent SSRF"""
    try:
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        return any(domain == allowed or domain.endswith('.' + allowed) for allowed in ALLOWED_DOMAINS)
    except Exception:
        return False

@app.route('/curl', methods=['GET'])
def curl():
    url = request.args.get('url')

    if not url:
        return jsonify({'error': 'URL parameter is required'}), 400

    if not is_url_allowed(url):
        return jsonify({'error': 'URL domain is not allowed'}), 400

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return jsonify({'url': url}), 200
    except requests.RequestException as e:
        return jsonify({'error': f'Failed to fetch URL: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
