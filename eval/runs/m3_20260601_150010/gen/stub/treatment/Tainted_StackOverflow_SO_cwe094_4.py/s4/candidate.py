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

    safe_dict = {
        '__builtins__': {},
        'abs': abs,
        'round': round,
        'min': min,
        'max': max,
        'sum': sum,
        'pow': pow,
        'sqrt': math.sqrt,
        'sin': math.sin,
        'cos': math.cos,
        'tan': math.tan,
        'pi': math.pi,
        'e': math.e,
    }

    try:
        result = eval(equation, safe_dict)
        return str(result)
    except:
        return ""
