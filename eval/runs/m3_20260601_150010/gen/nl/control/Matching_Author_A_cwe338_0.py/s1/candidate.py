from flask import Flask, session
import random

app = Flask(__name__)
app.secret_key = 'secret-key'

@app.route('/session')
def session_endpoint():
    random_number = random.randint(1, 100)
    session['random_number'] = random_number
    return {'random_number': random_number}

if __name__ == '__main__':
    app.run()
