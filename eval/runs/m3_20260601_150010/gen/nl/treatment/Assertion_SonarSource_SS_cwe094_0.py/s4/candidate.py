from flask import Flask, request, escape

app = Flask(__name__)

@app.route('/hello')
def hello():
    username = request.args.get('username', '')
    escaped_username = escape(username)
    template = "<p>Hello {username}</p>"
    return template.format(username=escaped_username)

if __name__ == '__main__':
    app.run()
