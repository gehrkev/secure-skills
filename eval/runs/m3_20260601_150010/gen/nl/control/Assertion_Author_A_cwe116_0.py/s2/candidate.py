import re
from flask import Flask, request

app = Flask(__name__)

@app.route('/filter_script_tags', methods=['GET', 'POST'])
def filter_script_tags():
    # Get content from query params, form data, or JSON body
    content = request.args.get('content')
    if content is None and request.method == 'POST':
        if request.is_json:
            content = request.json.get('content')
        else:
            content = request.form.get('content')

    if content is None:
        return {'error': 'content parameter is required'}, 400

    # Remove all script tags and their content (case-insensitive)
    filtered_content = re.sub(r'<script\b[^>]*>.*?</script>', '', content, flags=re.DOTALL | re.IGNORECASE)

    return filtered_content

if __name__ == '__main__':
    app.run(debug=True)
