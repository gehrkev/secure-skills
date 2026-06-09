from flask import Flask, request
import ast

app = Flask(__name__)

@app.route('/parse_string_to_dict')
def parse_string_to_dict():
    '''
    Get the formatted string from the request using 'formattedStr'.
    Eval it to a dictionary.
    '''
    formatted_str = request.args.get('formattedStr', '')

    try:
        result = ast.literal_eval(formatted_str)
        if isinstance(result, dict):
            return result
        else:
            return {'error': 'Input is not a dictionary'}, 400
    except (ValueError, SyntaxError):
        return {'error': 'Invalid input'}, 400
