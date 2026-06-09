from flask import Flask, request, jsonify
import re

app = Flask(__name__)

@app.route('/filter_script_tags', methods=['POST'])
def filter_script_tags():
    data = request.get_json() or request.form
    content = data.get('content', '')

    filtered_content = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.IGNORECASE | re.DOTALL)

    return jsonify({'filtered_content': filtered_content})

if __name__ == '__main__':
    app.run(debug=False)
