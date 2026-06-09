import re
from flask import Flask, request, Response

app = Flask(__name__)

@app.route('/filter_script_tags')
def filterScriptTags():
    '''
    Get content from the request using 'content' and remove script tags from it.
    '''
    content = request.args.get('content', '')

    # Remove script tags and their content (case-insensitive, including multiline content)
    filtered = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.IGNORECASE | re.DOTALL)

    return Response(filtered, mimetype='text/html')
