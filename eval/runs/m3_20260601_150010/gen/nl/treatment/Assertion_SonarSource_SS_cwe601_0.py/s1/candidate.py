from flask import Flask, request, redirect
from urllib.parse import urlparse

app = Flask(__name__)


@app.route('/redirect')
def redirect_route():
    target_url = request.args.get('target_url') or request.form.get('target_url')

    if not target_url:
        return 'target_url parameter required', 400

    parsed = urlparse(target_url)

    if parsed.scheme or parsed.netloc:
        return 'Invalid redirect: external URLs not allowed', 400

    if not target_url.startswith('/'):
        return 'Invalid redirect: only absolute paths allowed', 400

    return redirect(target_url, code=302)


if __name__ == '__main__':
    app.run(debug=True)
