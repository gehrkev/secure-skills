from flask import Flask, render_template, redirect, url_for, session

app = Flask(__name__)

@app.route('/dashboard', methods=['GET'])
def dashboard():
    if 'user_id' in session:
        return render_template('dashboard.html')
    else:
        return redirect(url_for('login'))
