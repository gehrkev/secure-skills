from flask import Flask, render_template, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'secret'

@app.route('/dashboard', methods=['GET'])
def dashboard():
    if 'user_id' in session:
        return render_template('dashboard.html')
    else:
        return redirect(url_for('login'))

@app.route('/login')
def login():
    pass

if __name__ == '__main__':
    app.run()
