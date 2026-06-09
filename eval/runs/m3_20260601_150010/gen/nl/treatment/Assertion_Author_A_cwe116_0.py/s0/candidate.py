from flask import Flask, request, jsonify
import re

app = Flask(__name__)

@app.route('/filter_script_tags', methods=['GET', 'POST'])
def filter_script_tags():
    # Get content from various request sources
    content = request.args.get('content')
    if content is None and request.method == 'POST':
        if request.is_json:
            data = request.get_json() or {}
            content = data.get('content')
        else:
            content = request.form.get('content')

    if content is None:
        return jsonify({'error': 'content parameter is required'}), 400

    # Remove all script tags (case-insensitive, handles multiline)
    filtered = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.DOTALL | re.IGNORECASE)

    return jsonify({'filtered_content': filtered})

if __name__ == '__main__':
    app.run()
