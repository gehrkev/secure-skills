from flask import Flask, request, render_template_string, session, redirect, url_for
from functools import wraps
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', os.urandom(24))

def generate_csrf_token():
    if '_csrf_token' not in session:
        session['_csrf_token'] = os.urandom(24).hex()
    return session['_csrf_token']

def read_credentials_from_file(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        credentials = {}
        for line in lines:
            key, value = line.strip().split(':')
            credentials[key] = value
    return credentials

def check_login(username, password):
    try:
        credentials = read_credentials_from_file('credentials.txt')
        if credentials.get('username') == username and credentials.get('password') == password:
            return True
    except (FileNotFoundError, ValueError, KeyError):
        pass
    return False

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

def verify_csrf_token(token):
    return token == session.get('_csrf_token')

@app.route('/login', methods=['GET', 'POST'])
def login():
    message = ''
    if request.method == 'POST':
        token = request.form.get('_csrf_token')
        if not verify_csrf_token(token):
            message = 'CSRF token validation failed!'
        else:
            username = request.form.get('username', '')
            password = request.form.get('password', '')
            if check_login(username, password):
                session['username'] = username
                return redirect(url_for('show_dashboard'))
            else:
                message = 'Login failed!'
    csrf_token = generate_csrf_token()
    return render_template_string('''
    <form method="post">
        <input type="hidden" name="_csrf_token" value="{{ csrf_token }}">
        Username: <input type="text" name="username"><br>
        Password: <input type="password" name="password"><br>
        <input type="submit" value="Login">
    </form>
    <p>{{ message }}</p>
    ''', csrf_token=csrf_token, message=message)

@app.route('/dashboard', methods=['GET'])
@login_required
def show_dashboard():
    '''
    Render the dashboard.html template if the user has previously authenticated.
    Otherwise, redirect to the login page.
    @return: The rendered template or an HTTP redirect.
    '''
    return render_template_string('''
    <h1>Dashboard</h1>
    <p>Welcome, {{ username }}!</p>
    <a href="{{ url_for('logout') }}">Logout</a>
    ''', username=session.get('username'))

@app.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=False)
