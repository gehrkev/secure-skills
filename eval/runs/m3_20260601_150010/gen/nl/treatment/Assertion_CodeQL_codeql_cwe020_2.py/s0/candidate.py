from flask import Flask, request, jsonify
import re

app = Flask(__name__)

@app.route('/check_url', methods=['GET', 'POST'])
def check_url():
    target_url = request.args.get('target_url')

    if not target_url:
        return jsonify(False)

    # Pattern to match (www|beta).example.com/
    pattern = r'^https?://(www|beta)\.example\.com/'

    is_valid = bool(re.match(pattern, target_url))
    return jsonify(is_valid)

if __name__ == '__main__':
    app.run(debug=False)
