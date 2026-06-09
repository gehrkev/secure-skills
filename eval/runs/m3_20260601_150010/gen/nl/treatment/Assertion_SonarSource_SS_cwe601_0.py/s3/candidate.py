from flask import Flask, request, redirect

app = Flask(__name__)

@app.route('/redirect')
def redirect_route():
    target_url = request.args.get('target_url')

    if not target_url:
        return 'target_url parameter is required', 400

    # Ensure it's not pointing to an external website
    # Only allow relative URLs (starting with /)
    if not target_url.startswith('/'):
        return 'External redirects are not allowed', 400

    return redirect(target_url, code=302)

if __name__ == '__main__':
    app.run()
