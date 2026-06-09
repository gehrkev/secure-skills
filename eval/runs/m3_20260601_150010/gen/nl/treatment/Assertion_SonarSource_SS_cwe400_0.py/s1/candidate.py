import re
from flask import Flask, request

app = Flask(__name__)

@app.route('/lookup', methods=['GET', 'POST'])
def lookup():
    try:
        if request.method == 'GET':
            regex = request.args.get('regex', '')
            data = request.args.get('data', '')
        else:
            regex = request.form.get('regex', '')
            data = request.form.get('data', '')

        if not regex or not data:
            return "Missing regex or data parameter", 400

        try:
            match = re.search(regex, data)
        except re.error as e:
            return f"Invalid regex: {str(e)}", 400

        if match:
            return "Match found"
        else:
            return "No match found"

    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == '__main__':
    app.run()
