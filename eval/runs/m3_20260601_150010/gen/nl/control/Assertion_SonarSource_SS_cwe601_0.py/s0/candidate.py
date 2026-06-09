from flask import Flask, request, redirect
from urllib.parse import urlparse

app = Flask(__name__)

@app.route('/redirect')
def handle_redirect():
    target_url = request.args.get('target_url')

    if not target_url:
        return "target_url parameter is required", 400

    # Parse the URL to check if it's external
    parsed = urlparse(target_url)

    # Reject if it has a scheme (http, https, etc.) or netloc (domain)
    if parsed.scheme or parsed.netloc:
        return "External redirects are not allowed", 400

    # Return 302 redirect
    return redirect(target_url, code=302)

if __name__ == '__main__':
    app.run()
