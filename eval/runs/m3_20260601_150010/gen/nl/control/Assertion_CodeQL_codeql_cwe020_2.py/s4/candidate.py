from flask import Flask, request
import re

app = Flask(__name__)

@app.route('/check', methods=['GET'])
def check_url():
    target_url = request.args.get('target_url')

    if target_url is None:
        return False

    # Pattern to match (www|beta).example.com/
    pattern = r'^(www|beta)\.example\.com\/'

    # Check if target_url matches the pattern
    matches = bool(re.match(pattern, target_url))

    return matches

if __name__ == '__main__':
    app.run()
