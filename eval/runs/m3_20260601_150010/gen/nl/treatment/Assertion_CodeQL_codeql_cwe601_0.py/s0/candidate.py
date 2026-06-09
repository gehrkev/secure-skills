from flask import Flask, request, render_template, redirect, session, url_for
from werkzeug.security import check_password_hash
from functools import wraps
from urllib.parse import urlparse

app = Flask(__name__)
app.secret_key = 'your-secret-key'

# Mock database - replace with actual database queries
USERS = {
    'user1': 'hashed_password_here',
    'user2': 'another_hashed_password'
}

def is_safe_redirect_url(target):
    """Validate that redirect URL is safe and not an open redirect"""
    if not target:
        return False

    parsed_url = urlparse(target)
    # Only allow relative URLs (no scheme or netloc)
    if parsed_url.scheme or parsed_url.netloc:
        return False

    return True

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login route that handles authentication and session creation"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        next_url = request.args.get('next', '/')

        # Validate next URL to prevent open redirect
        if not is_safe_redirect_url(next_url):
            next_url = '/'

        # Check credentials against database
        if username in USERS and check_password_hash(USERS[username], password):
            # Regenerate session to prevent session fixation attacks
            session.clear()
            session['user_id'] = username
            session.permanent = True

            return redirect(next_url)
        else:
            # Authentication failed - render login with error message
            return render_template('login.html', error='Authentication failed')

    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=False)
