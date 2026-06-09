from flask import Flask, request, redirect
from urllib.parse import urlparse

app = Flask(__name__)

@app.route('/redirect')
def redirect_route():
    target_url = request.args.get('target_url')

    if not target_url:
        return "No target_url provided", 400

    # Check if it's an external URL
    if target_url.startswith('//'):
        return "External URLs not allowed", 400

    parsed = urlparse(target_url)

    # If it has a scheme, it's external
    if parsed.scheme:
        return "External URLs not allowed", 400

    # Return 302 redirect
    return redirect(target_url, code=302)

if __name__ == '__main__':
    app.run()
