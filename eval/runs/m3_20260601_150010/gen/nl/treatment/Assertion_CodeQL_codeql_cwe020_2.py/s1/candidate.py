from flask import Flask, request, jsonify
import re

app = Flask(__name__)

@app.route('/check_url', methods=['GET', 'POST'])
def check_url():
    target_url = request.args.get('target_url') or request.form.get('target_url', '')

    pattern = r'^(www|beta)\.example\.com/'

    matches = bool(re.match(pattern, target_url))

    return jsonify({'result': matches})

if __name__ == '__main__':
    app.run(debug=False)
