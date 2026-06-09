from flask import Flask, request
from markupsafe import escape

app = Flask(__name__)

@app.route('/hello', methods=['GET', 'POST'])
def hello():
    username = request.args.get('username', '') or request.form.get('username', '')
    escaped_username = escape(username)
    template_string = "<p>Hello {username}</p>".format(username=escaped_username)
    return template_string

if __name__ == '__main__':
    app.run()
