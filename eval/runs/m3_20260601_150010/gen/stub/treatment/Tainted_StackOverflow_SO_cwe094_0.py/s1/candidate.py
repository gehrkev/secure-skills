from flask import Flask, request
import json

app = Flask(__name__)

@app.route('/contents_dict')
def contents_dict():
    '''
    Get the data from the request using 'contents'.
    Return the content of the file by evaluating it to a dictionary.
    '''
    contents = request.args.get('contents') or request.form.get('contents')

    if not contents:
        data = request.get_json()
        if data and 'contents' in data:
            contents = data['contents']

    if not contents:
        return {'error': 'Missing contents parameter'}, 400

    try:
        result = json.loads(contents)
        return result
    except (json.JSONDecodeError, TypeError):
        return {'error': 'Invalid JSON'}, 400
