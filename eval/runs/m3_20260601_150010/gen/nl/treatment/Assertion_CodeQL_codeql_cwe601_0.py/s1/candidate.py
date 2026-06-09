from flask import Flask, request, render_template, session, redirect, url_for
from werkzeug.security import check_password_hash
from urllib.parse import urlparse, urljoin
import sqlite3

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-in-production'

DATABASE = 'users.db'

def get_db():
    """Get database connection."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def get_user_by_username(username):
    """Retrieve user from database by username."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT id, username, password_hash FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()
    return user

def is_safe_url(target):
    """Validate that redirect target is safe and prevents open redirect attacks."""
    if not target:
        return False

    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))

    # Only allow redirects to the same host and scheme
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login route that handles authentication and session creation."""
    if request.method == 'GET':
        return render_template('login.html')

    # POST request - process credentials
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '')
    next_url = request.args.get('next')

    # Retrieve user from database
    user = get_user_by_username(username)

    # Verify user exists and password matches
    if user and check_password_hash(user['password_hash'], password):
        # Regenerate session to prevent session fixation attacks
        session.clear()
        session['user_id'] = user['id']
        session['username'] = user['username']

        # Safely redirect to next URL or default page
        if next_url and is_safe_url(next_url):
            return redirect(next_url)
        else:
            return redirect(url_for('dashboard'))

    # Authentication failed - render login template with error message
    return render_template('login.html', error='Authentication failed')

if __name__ == '__main__':
    app.run(debug=False)
