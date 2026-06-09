import re
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/check', methods=['GET', 'POST'])
def check_url():
    target_url = request.args.get('target_url') or request.form.get('target_url')

    if target_url is None:
        return jsonify(False), 400

    pattern = r'^(www|beta)\.example\.com/$'
    match = bool(re.match(pattern, target_url))

    return jsonify(match)

if __name__ == '__main__':
    app.run()
