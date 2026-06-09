from flask import Flask, session
from secrets import randint
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-key')

@app.route('/session')
def session_endpoint():
    random_number = randint(0, 999999)
    session['random_number'] = random_number
    return {'random_number': random_number}

if __name__ == '__main__':
    app.run()
