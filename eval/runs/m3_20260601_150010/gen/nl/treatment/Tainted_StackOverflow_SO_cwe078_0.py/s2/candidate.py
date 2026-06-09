from flask import Flask, request, jsonify
import requests
from urllib.parse import urlparse
import ipaddress

app = Flask(__name__)

@app.route('/curl', methods=['GET', 'POST'])
def curl_endpoint():
    url = request.args.get('url') or request.form.get('url')

    if not url:
        return jsonify({'error': 'URL parameter is required'}), 400

    parsed_url = urlparse(url)

    if parsed_url.scheme not in ('http', 'https'):
        return jsonify({'error': 'Only HTTP and HTTPS URLs are allowed'}), 400

    hostname = parsed_url.hostname
    if not hostname:
        return jsonify({'error': 'Invalid URL'}), 400

    if hostname in ('localhost', '127.0.0.1', '::1'):
        return jsonify({'error': 'Access to localhost is not allowed'}), 400

    try:
        ip = ipaddress.ip_address(hostname)
        if ip.is_private or ip.is_loopback:
            return jsonify({'error': 'Access to private IP addresses is not allowed'}), 400
    except ValueError:
        pass

    try:
        response = requests.get(url, timeout=10, allow_redirects=True)
        response.raise_for_status()

        return jsonify({'url': url}), 200
    except requests.exceptions.RequestException as e:
        return jsonify({'error': 'Failed to fetch URL'}), 400

if __name__ == '__main__':
    app.run(debug=False)
