from flask import Flask, render_template, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your-secret-key'

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
    app.run()
