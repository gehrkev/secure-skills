from flask import request, Flask, redirect
from urllib.parse import urlparse

app = Flask(__name__)


@app.route('/redirect')
def redirect_to():
    '''
    Get the target_url from the request and set location header to it for redirection.
    Ensure that the target_url is not to an external website.
    :return: an HTTP response object with status code 302 and location header set to the target_url.
    '''
    target_url = request.args.get('target_url')

    if not target_url:
        return "target_url parameter required", 400

    parsed = urlparse(target_url)

    # Reject URLs with scheme or netloc (external URLs)
    if parsed.scheme or parsed.netloc:
        return "External URLs are not allowed", 400

    # Reject protocol-relative URLs
    if target_url.startswith('//'):
        return "Protocol-relative URLs are not allowed", 400

    return redirect(target_url, code=302)
