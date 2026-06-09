import secrets
from flask import Flask, session, jsonify

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

@app.route('/session')
def generate_session():
    random_number = secrets.randbelow(2**31)
    session['random_number'] = random_number
    return jsonify(random_number=random_number)

if __name__ == '__main__':
    app.run()
