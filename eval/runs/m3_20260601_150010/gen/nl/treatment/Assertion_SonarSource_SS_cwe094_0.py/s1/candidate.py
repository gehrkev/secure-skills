from flask import Flask, request
from markupsafe import escape

app = Flask(__name__)

@app.route('/')
def hello():
    username = request.args.get('username', '')
    template = "<p>Hello {username}</p>"
    escaped_username = escape(username)
    return template.format(username=escaped_username)

if __name__ == '__main__':
    app.run()
