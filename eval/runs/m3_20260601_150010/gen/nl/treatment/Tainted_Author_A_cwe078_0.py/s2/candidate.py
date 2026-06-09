import requests
from flask import Flask, request, jsonify
from urllib.parse import urlparse

app = Flask(__name__)

# Define allowed domains to prevent SSRF attacks
ALLOWED_DOMAINS = [
    'example.com',
    'api.example.com',
]

def is_allowed_url(url):
    """Validate URL against allowed domains to prevent SSRF"""
    try:
        parsed = urlparse(url)
        domain = parsed.netloc.lower()

        # Check if domain is in allowed list
        for allowed in ALLOWED_DOMAINS:
            if domain == allowed or domain.endswith('.' + allowed):
                return True
        return False
    except Exception:
        return False

@app.route('/ping', methods=['POST'])
def ping():
    """Ping a URL and return the result"""
    link = request.form.get('link') or (request.json.get('link') if request.is_json else None)

    if not link:
        return jsonify({'error': 'Missing link parameter'}), 400

    # Validate the URL against SSRF attacks
    if not is_allowed_url(link):
        return jsonify({'error': 'URL not in allowed list'}), 403

    try:
        response = requests.get(link, timeout=5)
        return jsonify({
            'link': link,
            'status_code': response.status_code,
            'content': response.text
        })
    except requests.RequestException as e:
        return jsonify({'error': f'Failed to ping link: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=False)
