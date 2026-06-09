import re
from flask import Flask, request, jsonify

app = Flask(__name__)

ALLOWED_URLS = {
    'www.example.com/': 'www',
    'beta.example.com/': 'beta'
}

@app.route('/check_url', methods=['GET', 'POST'])
def check_url():
    target_url = request.args.get('target_url') or request.form.get('target_url')

    if not target_url:
        return jsonify({'result': False, 'error': 'target_url parameter is required'}), 400

    pattern = r'^(www|beta)\.example\.com/$'

    is_valid = bool(re.match(pattern, target_url))

    return jsonify({'result': is_valid})

if __name__ == '__main__':
    app.run(debug=False)
