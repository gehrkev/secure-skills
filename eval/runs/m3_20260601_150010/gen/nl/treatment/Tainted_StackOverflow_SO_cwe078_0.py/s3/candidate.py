import requests
from flask import Flask, request, abort

app = Flask(__name__)

ALLOWED_URLS = [
    'https://example.com',
    'https://api.example.com',
]

def is_url_allowed(url):
    """Check if the URL is in the allowed list"""
    for allowed in ALLOWED_URLS:
        if url.startswith(allowed):
            return True
    return False

@app.route('/curl', methods=['GET'])
def curl_endpoint():
    url = request.args.get('url')

    if not url:
        abort(400, description="Missing 'url' parameter")

    if not is_url_allowed(url):
        abort(403, description="URL not in allowed list")

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.content, response.status_code, {'Content-Type': response.headers.get('Content-Type', 'application/octet-stream')}
    except requests.RequestException as e:
        abort(502, description=f"Failed to fetch URL: {str(e)}")

if __name__ == '__main__':
    app.run(debug=False)
