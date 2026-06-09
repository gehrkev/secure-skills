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

    start = file_contents.find('{')
    end = file_contents.rfind('}')

    if start == -1 or end == -1 or start >= end:
        return {}

    json_str = file_contents[start:end+1]

    try:
        return json.loads(json_str)
    except json.JSONDecodeError:
        return {}
