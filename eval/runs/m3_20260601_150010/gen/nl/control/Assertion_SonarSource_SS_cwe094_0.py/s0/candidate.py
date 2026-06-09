from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def hello():
    username = request.args.get('username', 'Guest')
    template = "<p>Hello {username}</p>"
    return template.format(username=username)

if __name__ == '__main__':
    app.run()
