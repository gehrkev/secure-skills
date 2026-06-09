import re
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/filter_script_tags', methods=['GET', 'POST'])
def filter_script_tags():
    # Retrieve content parameter from various sources
    if request.method == 'POST':
        data = request.get_json(silent=True) or request.form
        content = data.get('content', '')
    else:
        content = request.args.get('content', '')

    # Remove all script tags (case-insensitive)
    filtered_content = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.IGNORECASE | re.DOTALL)

    return jsonify({'filtered_content': filtered_content})

if __name__ == '__main__':
    app.run(debug=True)
