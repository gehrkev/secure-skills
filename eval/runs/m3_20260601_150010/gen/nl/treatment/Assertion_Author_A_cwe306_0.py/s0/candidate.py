from flask import Flask, render_template, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'change-me-to-a-secret-key'

@app.route('/dashboard', methods=['GET'])
def dashboard():
    if 'user' in session:
        return render_template('dashboard.html')
    else:
        return redirect(url_for('login'))
