from flask import Flask, session
import secrets
import os

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

@app.route('/session')
def session_endpoint():
    random_number = secrets.randbelow(1000000)
    session['random_number'] = random_number
    return {'random_number': random_number}

if __name__ == '__main__':
    app.run(debug=True)
