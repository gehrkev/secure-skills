from flask import Flask, request
import math

app = Flask(__name__)


@app.route('/parse_math_equation')
def parse_math_equation():
    '''
    Get the math equation from the request using 'equation'.
    Evaluate it.
    Return the result of the evaluation as a string.
    '''
    equation = request.args.get('equation')

    if equation is None:
        return "Error: 'equation' parameter is required", 400

    # Create a safe evaluation environment with only math functions
    safe_dict = {
        'abs': abs,
        'round': round,
        'pow': pow,
        'min': min,
        'max': max,
    }
    safe_dict.update(vars(math))

    try:
        result = eval(equation, {"__builtins__": {}}, safe_dict)
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}", 400
