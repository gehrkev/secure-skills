from flask import Flask, request, render_template, redirect, session, url_for
from werkzeug.security import check_password_hash
from urllib.parse import urlparse
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')

# Placeholder for database connection - replace with your actual database
# from your_db_module import get_user_by_username

def get_user_by_username(username):
    """Query database for user by username. Replace with actual database implementation."""
    pass

def is_safe_redirect_url(target):
    """
    Validate that the target URL is safe for redirection to prevent open redirect attacks.
    Only allows relative URLs within the same origin.
    """
    if not target:
        return False
    parsed_url = urlparse(target)
    # Reject URLs with scheme or netloc to prevent redirects to external sites
    return not parsed_url.scheme and not parsed_url.netloc

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Login route that authenticates users and creates sessions.
    Prevents session fixation by clearing and regenerating session IDs.
    Prevents open redirects by validating the next URL.
    """
    if request.method == 'GET':
        return render_template('login.html')

    # Extract credentials from request
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '')
    next_url = request.args.get('next', '') or request.form.get('next', '')

    # Query database for user
    user = get_user_by_username(username)

    # Verify credentials
    if user and check_password_hash(user.password_hash, password):
        # Clear old session to prevent session fixation attacks
        session.clear()

        # Create new session for authenticated user
        session['user_id'] = user.id
        session.permanent = True

        # Safely redirect to next URL or default destination
        if next_url and is_safe_redirect_url(next_url):
            return redirect(next_url)
        else:
            return redirect(url_for('index'))

    # Authentication failed - render login page with error message
    return render_template('login.html', error='Authentication failed')
