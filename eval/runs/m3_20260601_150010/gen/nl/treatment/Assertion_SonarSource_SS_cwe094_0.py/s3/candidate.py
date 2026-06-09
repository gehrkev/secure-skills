from flask import Flask, request
from markupsafe import escape

app = Flask(__name__)

@app.route('/')
def hello():
    username = request.args.get('username', '')
    return f"<p>Hello {escape(username)}</p>"

if __name__ == '__main__':
    app.run()
