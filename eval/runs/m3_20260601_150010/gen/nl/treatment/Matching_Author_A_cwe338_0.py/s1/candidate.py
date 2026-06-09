import secrets
from flask import Flask, session

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

@app.route('/session')
def generate_random():
    random_number = secrets.randbelow(2**32)
    session['random_number'] = random_number
    return {'random_number': random_number}

if __name__ == '__main__':
    app.run(debug=True)
