from flask import Flask, request

app = Flask(__name__)

@app.route('/open_file', methods=['GET', 'POST'])
def open_file():
    filename = request.args.get('filename') or request.form.get('filename')

    if not filename:
        return None

    try:
        return open(filename, 'r')
    except:
        return None
