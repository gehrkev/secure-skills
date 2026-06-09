from flask import Flask, request

app = Flask(__name__)

@app.route('/open_file')
def open_file():
    file_name = request.args.get('file_name')
    if not file_name:
        return None

    try:
        return open(file_name, 'r')
    except:
        return None
