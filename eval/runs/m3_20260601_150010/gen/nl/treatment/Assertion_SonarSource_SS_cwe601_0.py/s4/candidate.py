from flask import Flask, request, redirect
from urllib.parse import urlparse

app = Flask(__name__)

ALLOWED_URLS = {
    1: '/home',
    2: '/dashboard',
    3: '/profile',
}

@app.route('/redirect')
def redirect_route():
    target_url = request.args.get('target_url')

    if not target_url:
        return 'Missing target_url parameter', 400

    parsed_url = urlparse(target_url)

    if parsed_url.netloc:
        return 'External redirects are not allowed', 403

    if not target_url.startswith('/'):
        return 'URL must be a relative path starting with /', 400

    return redirect(target_url, code=302)


if __name__ == '__main__':
    app.run(debug=False)
