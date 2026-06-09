from flask import Flask, request
import re

app = Flask(__name__)

@app.route('/lookup', methods=['GET', 'POST'])
def lookup():
    regex = request.args.get('regex') or request.form.get('regex', '')
    data = request.args.get('data') or request.form.get('data', '')

    if not regex or not data:
        return "Error: regex and data parameters required", 400

    if len(regex) > 1000:
        return "Error: regex pattern too long", 400

    try:
        if re.search(regex, data):
            return "Match found"
        else:
            return "No match found"
    except re.error:
        return "Error: Invalid regex pattern", 400

if __name__ == '__main__':
    app.run(debug=False)
