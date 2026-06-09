import re
from flask import Flask, request

app = Flask(__name__)

@app.route('/lookup', methods=['GET', 'POST'])
def lookup():
    regex = request.args.get('regex') or request.form.get('regex')
    data = request.args.get('data') or request.form.get('data')

    if not regex or not data:
        return "Missing regex or data parameter", 400

    try:
        if re.search(regex, data):
            return "Match found"
        else:
            return "No match found"
    except re.error:
        return "Invalid regex pattern", 400

if __name__ == '__main__':
    app.run(debug=True)
