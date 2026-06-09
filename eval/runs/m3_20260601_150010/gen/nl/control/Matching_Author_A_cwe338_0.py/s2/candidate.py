from flask import Flask, session
import random
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/session')
def store_random_in_session():
    random_number = random.randint(0, 100)
    session['random_number'] = random_number
    return {'random_number': random_number}

if __name__ == '__main__':
    app.run()
