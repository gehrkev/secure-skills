from flask import Flask, request, redirect
from urllib.parse import urlparse

app = Flask(__name__)

@app.route('/redirect')
def redirect_route():
    target_url = request.args.get('target_url')

    if not target_url:
        return "No target URL provided", 400

    # Check if URL is external (has a network location)
    parsed = urlparse(target_url)
    if parsed.netloc:
        return "External URLs not allowed", 400

    return redirect(target_url, code=302)

if __name__ == '__main__':
    app.run()
