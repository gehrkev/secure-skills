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
    equation = request.args.get('equation', '')

    # Safe namespace with only mathematical operations
    safe_dict = {
        'sin': math.sin,
        'cos': math.cos,
        'tan': math.tan,
        'sqrt': math.sqrt,
        'log': math.log,
        'exp': math.exp,
        'pi': math.pi,
        'e': math.e,
        '__builtins__': {}
    }

    try:
        result = eval(equation, safe_dict)
        return str(result)
    except Exception:
        return "Error evaluating equation"
