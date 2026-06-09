from flask import Flask, session
import random

app = Flask(__name__)
app.secret_key = 'secret-key-for-sessions'

@app.route('/session')
def session_endpoint():
    random_number = random.randint(0, 1000000)
    session['random_number'] = random_number
    return {'random_number': random_number}

if __name__ == '__main__':
    app.run()
