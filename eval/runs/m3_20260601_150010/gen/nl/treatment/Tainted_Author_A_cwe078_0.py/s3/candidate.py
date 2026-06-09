from flask import Flask, request, jsonify
import requests
from urllib.parse import urlparse

app = Flask(__name__)

ALLOWED_DOMAINS = [
    'example.com',
    'api.example.com',
]

def is_url_allowed(url):
    """Validate URL against allowlist to prevent SSRF attacks."""
    try:
        parsed = urlparse(url)
        domain = parsed.netloc
        return domain in ALLOWED_DOMAINS
    except:
        return False

@app.route('/ping', methods=['POST'])
def ping():
    """Ping a link and return the result."""
    link = request.form.get('link') or request.json.get('link')

    if not link:
        return jsonify({'error': 'Missing link parameter'}), 400

    if not is_url_allowed(link):
        return jsonify({'error': 'Invalid or unauthorized URL'}), 400

    try:
        response = requests.get(link, timeout=5)
        return jsonify({
            'link': link,
            'status_code': response.status_code,
            'content': response.text
        })
    except requests.RequestException:
        return jsonify({'error': 'Failed to fetch content'}), 500

if __name__ == '__main__':
    app.run()
