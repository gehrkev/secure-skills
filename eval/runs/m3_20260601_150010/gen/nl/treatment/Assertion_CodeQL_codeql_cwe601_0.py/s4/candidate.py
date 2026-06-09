from flask import Flask, request, render_template, redirect, session, url_for
from werkzeug.security import check_password_hash
from urllib.parse import urlparse, urljoin
import secrets

app = Flask(__name__)
app.secret_key = 'your-secret-key'

# Mock database - in production, use actual database with hashed passwords
USERS = {
    'testuser': 'hashed_password_hash_here'
}

def is_safe_url(target):
    """Validate that redirect target is safe (same-origin or relative)."""
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))

    # Ensure URL is relative or same-origin to prevent open redirect (CWE-601)
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        next_url = request.form.get('next') or request.args.get('next')

        # Check credentials against database
        if username in USERS and check_password_hash(USERS[username], password):
            # Regenerate session to prevent session fixation (CWE-384)
            session.clear()
            session['user_id'] = username
            session['_csrf_token'] = secrets.token_hex(16)

            # Safely redirect to next URL if provided
            if next_url and is_safe_url(next_url):
                return redirect(next_url)

            return redirect(url_for('dashboard'))
        else:
            # Authentication failed
            return render_template('login.html', error='Authentication failed')

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    # Check user is authenticated
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')
