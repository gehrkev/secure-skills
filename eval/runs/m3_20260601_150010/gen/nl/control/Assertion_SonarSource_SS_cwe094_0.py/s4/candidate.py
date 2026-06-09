from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def hello():
    username = request.args.get('username', 'Guest')
    return f"<p>Hello {username}</p>"

if __name__ == '__main__':
    app.run()
