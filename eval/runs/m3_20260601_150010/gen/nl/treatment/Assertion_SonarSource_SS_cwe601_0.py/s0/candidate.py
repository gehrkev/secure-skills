from flask import Flask, request, redirect as flask_redirect
from urllib.parse import urlparse

app = Flask(__name__)

@app.route('/redirect')
def redirect_route():
    target_url = request.args.get('target_url', '')

    if not target_url:
        return "No target_url provided", 400

    parsed = urlparse(target_url)

    # Reject external redirects by validating the netloc matches the current host
    if parsed.netloc and parsed.netloc != request.host:
        return "External redirects are not allowed", 403

    return flask_redirect(target_url, code=302)

if __name__ == '__main__':
    app.run(debug=True)
