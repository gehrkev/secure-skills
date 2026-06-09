import re
from flask import Flask, request

app = Flask(__name__)

@app.route('/filter_script_tags', methods=['GET', 'POST'])
def filter_script_tags():
    content = request.args.get('content') or request.form.get('content', '')
    filtered_content = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.IGNORECASE | re.DOTALL)
    return filtered_content

if __name__ == '__main__':
    app.run()
