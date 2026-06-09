from flask import Flask, session, render_template, redirect, url_for

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

@app.route('/dashboard', methods=['GET'])
def dashboard():
    if 'user_id' in session:
        return render_template('dashboard.html')
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
