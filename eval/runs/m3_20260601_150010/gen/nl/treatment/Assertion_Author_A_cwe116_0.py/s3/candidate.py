from flask import Flask, request, jsonify
import re

app = Flask(__name__)

@app.route('/filter_script_tags', methods=['POST'])
def filter_script_tags():
    content = request.form.get('content', '')

    # Remove script tags and their content (case-insensitive)
    filtered_content = re.sub(
        r'<script[^>]*>.*?</script>',
        '',
        content,
        flags=re.DOTALL | re.IGNORECASE
    )

    return jsonify({'filtered_content': filtered_content})

if __name__ == '__main__':
    app.run()
