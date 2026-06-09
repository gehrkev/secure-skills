import re
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/validate_url', methods=['GET', 'POST'])
def validate_url():
    target_url = request.args.get('target_url') or request.form.get('target_url')

    if not target_url:
        return jsonify({'valid': False}), 400

    pattern = r'^(www|beta)\.example\.com/'
    is_valid = bool(re.match(pattern, target_url))

    return jsonify({'valid': is_valid})

if __name__ == '__main__':
    app.run(debug=False)
