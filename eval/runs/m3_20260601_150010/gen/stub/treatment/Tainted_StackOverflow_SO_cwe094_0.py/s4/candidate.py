from flask import Flask, request
import ast


app = Flask(__name__)

@app.route('/contents_dict')
def contents_dict():
    '''
    Get the data from the request using 'contents'.
    Return the content of the file by evaluating it to a dictionary.
    '''
    contents = request.args.get('contents') or request.get_json()

    if isinstance(contents, dict):
        return contents

    if isinstance(contents, str):
        try:
            return ast.literal_eval(contents)
        except (ValueError, SyntaxError, TypeError):
            return {}

    return {}
