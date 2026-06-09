from flask import Flask, request
import re

app = Flask(__name__)

@app.route('/filter_script_tags', methods=['GET', 'POST'])
def filter_script_tags():
    content = request.args.get('content') or request.form.get('content') or ''
    filtered = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.IGNORECASE | re.DOTALL)
    return filtered

if __name__ == '__main__':
    app.run()
