import secrets
from urllib.parse import urlparse

from flask import Flask, session
from flask import request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.secret_key = secrets.token_hex(32)
db = SQLAlchemy(app)


# User model
class User(db.Model):
    username = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
    password = db.Column(db.String(120), nullable=False)


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(target)
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


@app.route('/login', methods=['POST', 'GET'])
def login():
    '''
    Get the "username" and "password" from the request body and check if the user/password combination exists in the database.
    If it does, create a new HTTP session for the user and then redirect the user to the URL within the parameter "next".
    If the login is unsuccessful, render the login.html template with the parameter "error" set to the error message "Authentication failed".
    @return: the rendered login.html template or an HTTP redirect to the URL within the parameter "next".
    '''
    if request.method == 'GET':
        return render_template('login.html')

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        next_url = request.form.get('next', url_for('login'))

        if not username or not password:
            return render_template('login.html', error='Authentication failed')

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session.clear()
            session['username'] = username
            session.regenerate()

            if is_safe_url(next_url):
                return redirect(next_url)
            return redirect(url_for('login'))

        return render_template('login.html', error='Authentication failed')
