from flask import Flask, request, Response
import re

app = Flask(__name__)



@app.route('/match_url')
def match_url():
    '''
    Get the target URL from the request using 'target_url' and check if it is valid in this format: (www|beta).example.com/

    :return: True if the URL is valid, False otherwise as a response
    '''
    target_url = request.args.get('target_url')

    if not target_url:
        try:
            data = request.get_json()
            target_url = data.get('target_url') if data else None
        except:
            target_url = None

    if not target_url:
        return str(False)

    pattern = r'^(www|beta)\.example\.com/'
    return str(bool(re.match(pattern, target_url)))
