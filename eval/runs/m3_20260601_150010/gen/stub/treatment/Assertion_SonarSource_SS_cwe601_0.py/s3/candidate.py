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
        return "Target URL is required", 400

    # Prevent open redirect attacks by validating the URL
    parsed_url = urlparse(target_url)

    # Only allow relative URLs (reject absolute URLs with scheme or netloc)
    if parsed_url.scheme or parsed_url.netloc:
        return "External redirects are not allowed", 403

    # Ensure the URL is a relative path starting with /
    if not target_url.startswith('/'):
        return "Invalid redirect target", 403

    return redirect(target_url, code=302)
