from flask import Flask, request, redirect
from urllib.parse import urlparse

app = Flask(__name__)

@app.route('/redirect', methods=['GET', 'POST'])
def redirect_route():
    target_url = request.args.get('target_url')

    if not target_url:
        return "target_url parameter is required", 400

    # Parse the target URL
    parsed = urlparse(target_url)

    # If the URL has a netloc (domain), ensure it matches the current host
    if parsed.netloc:
        current_host = request.host.split(':')[0]  # Remove port
        target_host = parsed.netloc.split(':')[0]
        if current_host != target_host:
            return "External URLs are not allowed", 403

    # Safe to redirect (relative URL or same-host absolute URL)
    return redirect(target_url, code=302)

if __name__ == '__main__':
    app.run()
