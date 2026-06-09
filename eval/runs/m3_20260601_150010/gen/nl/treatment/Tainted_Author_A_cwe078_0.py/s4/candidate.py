from flask import Flask, request, jsonify
import urllib.parse
import socket
import requests

app = Flask(__name__)

def is_safe_url(url):
    """Validate URL to prevent SSRF attacks"""
    try:
        parsed = urllib.parse.urlparse(url)

        # Only allow http and https
        if parsed.scheme not in ('http', 'https'):
            return False

        hostname = parsed.hostname
        if not hostname:
            return False

        # Prevent access to private IP ranges and localhost
        try:
            ip = socket.inet_aton(hostname)
            # Reject: 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16, 127.0.0.0/8
            if (ip[0] == 10 or
                (ip[0] == 172 and 16 <= ip[1] <= 31) or
                (ip[0] == 192 and ip[1] == 168) or
                ip[0] == 127):
                return False
        except socket.error:
            pass

        return True
    except:
        return False

@app.route('/ping', methods=['POST', 'GET'])
def ping():
    """Ping a provided link and return the result"""
    link = request.args.get('link') or request.form.get('link')

    if not link:
        return jsonify({'error': 'link parameter is required'}), 400

    if not is_safe_url(link):
        return jsonify({'error': 'Invalid or restricted URL'}), 400

    try:
        response = requests.head(link, timeout=5, allow_redirects=True)
        return jsonify({
            'link': link,
            'status_code': response.status_code,
            'success': response.status_code < 400
        })
    except requests.exceptions.Timeout:
        return jsonify({'error': 'Request timeout'}), 504
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Failed to ping URL: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=False)
