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
        return {'error': 'Missing contents parameter'}, 400

    try:
        data = json.loads(contents)
        if isinstance(data, dict):
            return data
        return {'error': 'Contents must be a JSON dictionary'}, 400
    except (json.JSONDecodeError, TypeError):
        return {'error': 'Invalid JSON'}, 400
