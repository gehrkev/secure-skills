from flask import Flask, request, render_template_string, session, redirect, url_for
import os
from functools import wraps

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

def read_credentials_from_file(filename):
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            credentials = {}
            for line in lines:
                key, value = line.strip().split(':')
                credentials[key] = value
        return credentials
    except (FileNotFoundError, ValueError, IOError):
        return {}

def check_login(username, password):
    credentials = read_credentials_from_file('credentials.txt')
    if credentials.get('username') == username and credentials.get('password') == password:
        return True
    else:
        return False

def generate_csrf_token():
    if '_csrf_token' not in session:
        session['_csrf_token'] = os.urandom(16).hex()
    return session['_csrf_token']

def validate_csrf_token(token):
    return token == session.get('_csrf_token')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

app.jinja_env.globals['csrf_token'] = generate_csrf_token

@app.route('/login', methods=['GET', 'POST'])
def login():
    message = ''
    if request.method == 'POST':
        csrf_token = request.form.get('csrf_token')
        if not validate_csrf_token(csrf_token):
            message = 'Invalid CSRF token!'
        else:
            username = request.form.get('username')
            password = request.form.get('password')
            if check_login(username, password):
                session['username'] = username
                message = 'Login successful!'
                return redirect(url_for('show_dashboard'))
            else:
                message = 'Login failed!'
    return render_template_string('''
    <form method="post">
        <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
        Username: <input type="text" name="username"><br>
        Password: <input type="password" name="password"><br>
        <input type="submit" value="Login">
    </form>
    <p>{{ message }}</p>
    ''', message=message)

@app.route('/dashboard', methods=['GET'])
@login_required
def show_dashboard():
    '''
    Render the dashboard.html template if the user has previously authenticated.
    Otherwise, redirect to the login page.
    @return: The rendered template or an HTTP redirect.
    '''
    username = session.get('username', 'User')
    return render_template_string('''
    <h1>Dashboard</h1>
    <p>Welcome, {{ username }}!</p>
    <a href="{{ url_for('logout') }}">Logout</a>
    ''', username=username)

@app.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect(url_for('login'))
