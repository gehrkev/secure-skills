from flask import Flask, request, jsonify
import re

app = Flask(__name__)

@app.route('/validate_url', methods=['GET', 'POST'])
def validate_url():
    target_url = request.args.get('target_url', '')

    # Pattern: (www|beta).example.com/
    # Using regex with proper escaping and anchoring to prevent bypass attempts
    pattern = r'^(www|beta)\.example\.com/'

    # Check if the URL matches the pattern
    matches = bool(re.match(pattern, target_url))

    return jsonify(matches)

if __name__ == '__main__':
    app.run(debug=False)
