import re
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/check')
def check_url():
    target_url = request.args.get('target_url', '')
    pattern = r'^(www|beta)\.example\.com/'
    matches = bool(re.match(pattern, target_url))
    return jsonify(matches)

if __name__ == '__main__':
    app.run()
