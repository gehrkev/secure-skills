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
    result = ast.literal_eval(formatted_str)
    return result
