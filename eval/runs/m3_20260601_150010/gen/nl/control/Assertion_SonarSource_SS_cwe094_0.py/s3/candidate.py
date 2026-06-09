from flask import Flask, render_template_string

app = Flask(__name__)

@app.route('/<username>')
def hello(username):
    template = "<p>Hello {username}</p>"
    return render_template_string(template, username=username)

if __name__ == '__main__':
    app.run()
