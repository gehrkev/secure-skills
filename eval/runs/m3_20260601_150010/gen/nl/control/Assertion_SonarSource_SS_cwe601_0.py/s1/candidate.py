from flask import Flask, request, redirect
from urllib.parse import urlparse

app = Flask(__name__)

@app.route('/redirect')
def redirect_route():
    target_url = request.args.get('target_url')

    if not target_url:
        return "target_url parameter is required", 400

    # Parse the target URL
    parsed = urlparse(target_url)

    # If it has a netloc (domain/host), validate it matches current host
    if parsed.netloc:
        # Extract hostname without port for comparison
        target_host = parsed.netloc.split(':')[0]
        current_host = request.host.split(':')[0]

        if target_host != current_host:
            return "target_url must be internal", 400

    # Redirect to the target URL with 302 status
    return redirect(target_url, code=302)

if __name__ == '__main__':
    app.run()
