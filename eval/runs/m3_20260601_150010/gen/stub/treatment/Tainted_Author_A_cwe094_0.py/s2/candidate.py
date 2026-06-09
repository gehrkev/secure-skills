from flask import Flask, request
import json

app = Flask(__name__)

@app.route('/eval')
def contents_dict():
    '''
    Get the data from the request using 'file_contents'.
    Remove anything before the first '{' and after the last '}'.
    Return the content by evaluating it to a dictionary.
    '''
    file_contents = request.args.get('file_contents', '')

    first_brace = file_contents.find('{')
    last_brace = file_contents.rfind('}')

    if first_brace == -1 or last_brace == -1 or first_brace > last_brace:
        return {}

    json_str = file_contents[first_brace:last_brace + 1]

    try:
        return json.loads(json_str)
    except (json.JSONDecodeError, ValueError):
        return {}
