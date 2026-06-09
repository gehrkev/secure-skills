from flask import Flask, request, render_template_string, session, render, redirect, url_for
from werkzeug.security import check_password_hash, generate_password_hash
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

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
        if credentials.get('username') == username:
            stored_password = credentials.get('password', '')
            if check_password_hash(stored_password, password):
                return True
    except (FileNotFoundError, KeyError, ValueError):
        pass
    return False

@app.route('/login', methods=['GET', 'POST'])
def login():
    message = ''
    if request.method == 'POST':
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
        Username: <input type="text" name="username"><br>
        Password: <input type="password" name="password"><br>
        <input type="submit" value="Login">
    </form>
    <p>{{ message }}</p>
    ''', message=message)


@app.route('/dashboard', methods=['GET'])
def show_dashboard():
    '''
    Render the dashboard.html template if the user has previously authenticated.
    Otherwise, redirect to the login page.
    @return: The rendered template or an HTTP redirect.
    '''
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template_string('''
    <h1>Dashboard</h1>
    <p>Welcome, {{ username }}!</p>
    <a href="{{ url_for('logout') }}">Logout</a>
    ''', username=session['username'])


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return redirect(url_for('login'))
