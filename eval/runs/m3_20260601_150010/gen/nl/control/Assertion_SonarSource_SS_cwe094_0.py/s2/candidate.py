from flask import Flask, request

app = Flask(__name__)

@app.route('/hello')
def hello():
    username = request.args.get('username', 'Guest')
    return f"<p>Hello {username}</p>"
