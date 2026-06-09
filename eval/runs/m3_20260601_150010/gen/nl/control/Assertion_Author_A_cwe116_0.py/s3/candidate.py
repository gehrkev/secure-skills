from flask import Flask, request
import re

app = Flask(__name__)

@app.route('/filter_script_tags', methods=['GET', 'POST'])
def filter_script_tags():
    content = request.args.get('content') or request.form.get('content')

    if content is None:
        return 'content parameter is required', 400

    # Remove script tags and their content
    filtered_content = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.DOTALL | re.IGNORECASE)

    return filtered_content

if __name__ == '__main__':
    app.run()
