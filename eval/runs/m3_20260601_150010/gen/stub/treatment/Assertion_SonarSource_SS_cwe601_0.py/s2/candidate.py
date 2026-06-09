from flask import request, Flask, redirect, Response
from urllib.parse import urlparse

app = Flask(__name__)


@app.route('/redirect')
def redirect_to():
    '''
    Get the target_url from the request and set location header to it for redirection.
    Ensure that the target_url is not to an external website.
    :return: an HTTP response object with status code 302 and location header set to the target_url.
    '''
    target_url = request.args.get('target_url') or request.form.get('target_url')

    if not target_url:
        return Response("Missing target_url", status=400)

    if target_url.startswith('//'):
        return Response("External URLs not allowed", status=400)

    parsed = urlparse(target_url)

    if parsed.scheme or parsed.netloc:
        return Response("External URLs not allowed", status=400)

    return redirect(target_url, code=302)
