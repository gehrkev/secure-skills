from flask import Flask, request, jsonify
import ast

app = Flask(__name__)


@app.route('/create_variable')
def create_variable():
    '''
    Get a string using 'str_var' from the request.
    Create a variable from the string.
    Return the variable.
    '''
    str_var = request.args.get('str_var', '')

    try:
        variable = ast.literal_eval(str_var)
    except (ValueError, SyntaxError):
        variable = str_var

    return jsonify({'variable': variable})
