from flask import Flask, request, session, redirect, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        next_url = request.form.get('next', '/')

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            return redirect(next_url)
        else:
            return render_template('login.html', error='Authentication failed')

    next_url = request.args.get('next', '/')
    return render_template('login.html', next=next_url)

if __name__ == '__main__':
    app.run(debug=True)
