from flask import Flask, request, redirect
from urllib.parse import urlparse

app = Flask(__name__)

@app.route('/redirect')
def handle_redirect():
    target_url = request.args.get('target_url')

    if not target_url:
        return 'target_url parameter is required', 400

    parsed = urlparse(target_url)

    # If URL has a netloc (domain), ensure it matches current domain
    if parsed.netloc:
        current_host = request.host.split(':')[0]
        target_host = parsed.netloc.split(':')[0]

        if current_host != target_host:
            return 'Redirect to external websites is not allowed', 400

    return redirect(target_url, code=302)

if __name__ == '__main__':
    app.run()
