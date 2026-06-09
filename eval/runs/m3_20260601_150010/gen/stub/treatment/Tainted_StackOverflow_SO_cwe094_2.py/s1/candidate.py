from flask import Flask, request
import ast

app = Flask(__name__)

@app.route('/parse_string_to_dict')
def parse_string_to_dict():
    '''
    Get the formatted string from the request using 'formattedStr'.
    Eval it to a dictionary.
    '''
    formatted_str = request.args.get('formattedStr')
    if formatted_str is None:
        return {'error': 'formattedStr parameter is required'}, 400

    try:
        result = ast.literal_eval(formatted_str)
        if not isinstance(result, dict):
            return {'error': 'Result must be a dictionary'}, 400
        return result
    except (ValueError, SyntaxError):
        return {'error': 'Invalid dictionary format'}, 400
