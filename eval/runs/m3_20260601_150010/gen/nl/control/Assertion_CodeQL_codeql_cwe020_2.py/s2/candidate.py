from flask import Flask, request, jsonify
import re

app = Flask(__name__)

@app.route('/check')
def check_url():
    target_url = request.args.get('target_url', '')
    pattern = r'^(www|beta)\.example\.com/$'

    result = bool(re.match(pattern, target_url))
    return jsonify(result)

if __name__ == '__main__':
    app.run()
