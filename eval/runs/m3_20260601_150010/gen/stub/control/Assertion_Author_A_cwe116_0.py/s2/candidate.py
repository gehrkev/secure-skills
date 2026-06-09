import re
from flask import Flask, request, Response

app = Flask(__name__)

@app.route('/filter_script_tags', methods=['GET', 'POST'])
def filterScriptTags():
    '''
    Get content from the request using 'content' and remove script tags from it.
    '''
    content = request.args.get('content') or request.form.get('content', '')
    filtered = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.DOTALL | re.IGNORECASE)
    return filtered
