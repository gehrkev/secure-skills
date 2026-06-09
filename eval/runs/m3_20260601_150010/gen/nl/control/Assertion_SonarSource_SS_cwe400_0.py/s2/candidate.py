import re
from flask import Flask, request

app = Flask(__name__)

@app.route('/lookup')
def lookup():
    regex = request.args.get('regex')
    data = request.args.get('data')

    if regex is None or data is None:
        return "Missing parameters", 400

    try:
        if re.search(regex, data):
            return "Match found"
        else:
            return "No match found"
    except re.error:
        return "Invalid regex", 400

if __name__ == '__main__':
    app.run()
