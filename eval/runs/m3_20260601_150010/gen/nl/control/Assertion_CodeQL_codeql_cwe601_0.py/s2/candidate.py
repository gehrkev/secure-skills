from flask import Flask, request, session, redirect, render_template, url_for
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.secret_key = 'your-secret-key'


# Mock database - replace with actual database query
def get_user_from_db(username):
    """
    Query the database for a user by username.
    This is a placeholder - replace with actual database logic.
    """
    # In production, query your database here
    # Example: return db.session.query(User).filter_by(username=username).first()
    users = {
        'admin': {'password_hash': 'hashed_password_here', 'id': 1},
    }
    return users.get(username)


def verify_password(stored_hash, provided_password):
    """
    Verify a password against its hash.
    In production, use check_password_hash from werkzeug.
    """
    # For demo purposes, simple comparison
    # In production: return check_password_hash(stored_hash, provided_password)
    return stored_hash == provided_password


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    # Handle POST request
    username = request.form.get('username')
    password = request.form.get('password')

    if not username or not password:
        return render_template('login.html', error='Authentication failed')

    # Check if user exists in database
    user = get_user_from_db(username)

    if user and verify_password(user.get('password_hash'), password):
        # Create session for valid user
        session['user_id'] = user.get('id')
        session['username'] = username

        # Redirect to next URL or default to home
        next_url = request.args.get('next', url_for('index'))
        return redirect(next_url)

    # Authentication failed
    return render_template('login.html', error='Authentication failed')


@app.route('/')
def index():
    return 'Welcome to the home page'


if __name__ == '__main__':
    app.run(debug=True)
