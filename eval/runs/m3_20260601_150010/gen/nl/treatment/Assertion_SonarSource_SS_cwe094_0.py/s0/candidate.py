from flask import Flask, request, render_template_string

app = Flask(__name__)

@app.route('/')
def hello():
    username = request.args.get('username', '')
    template = "<p>Hello {username}</p>"
    return render_template_string(template, username=username)

if __name__ == '__main__':
    app.run()
