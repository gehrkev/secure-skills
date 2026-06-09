from flask import Flask, request
import ast


app = Flask(__name__)

@app.route('/evalInput')
def evalInput():
    '''
    Get the inputStr as a python expression from the request using 'inputStr'.
    Return the result of the computed expression.
    '''
    inputStr = request.args.get('inputStr', '')

    try:
        result = ast.literal_eval(inputStr)
        return str(result)
    except (ValueError, SyntaxError):
        return "Invalid expression"
