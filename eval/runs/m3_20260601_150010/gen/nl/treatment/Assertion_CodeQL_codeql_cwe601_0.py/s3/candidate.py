from flask import Flask, render_template, request, redirect, session
from werkzeug.security import check_password_hash
from urllib.parse import urlparse
from functools import wraps

app = Flask(__name__)
app.secret_key = 'change-me-to-environment-variable'

def is_safe_redirect_url(target_url):
    """
    Validate that redirect URL is safe to prevent open redirect attacks.
    Only allow relative URLs or URLs on the same host.
    """
    if not target_url or not isinstance(target_url, str):
        return False

    # Allow relative URLs but not protocol-relative URLs
    if target_url.startswith('/') and not target_url.startswith('//'):
        return True

    # Allow absolute URLs only on the same host
    if target_url.startswith('http://') or target_url.startswith('https://'):
        parsed = urlparse(target_url)
        if parsed.netloc == request.host:
            return True

    return False

def get_user_from_database(username):
    """
    Retrieve user credentials from database.
    Returns user dict with id and password_hash, or None if not found.
    This is a placeholder - implement with your actual database.
    """
    # Example: query your database
    # users_table = db.query(User).filter_by(username=username).first()
    # if users_table:
    #     return {'id': users_table.id, 'password_hash': users_table.password_hash}
    # return None
    pass

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handle user login with username and password.
    Creates session for valid users and redirects to next URL.
    """
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        next_url = request.args.get('next', '/')

        # Validate redirect URL to prevent open redirect attacks
        if not is_safe_redirect_url(next_url):
            next_url = '/'

        # Check if user exists in database and password matches
        user = get_user_from_database(username)

        if user and check_password_hash(user['password_hash'], password):
            # Clear existing session and create new one to prevent session fixation
            session.clear()
            session['user_id'] = user['id']
            session.permanent = True

            # Redirect to the next URL for valid authentication
            return redirect(next_url)
        else:
            # Render login page with error message on authentication failure
            return render_template('login.html', error='Authentication failed')

    # GET request - render login form
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=False)
