from flask import Flask, request

app = Flask(__name__)


@app.route('/parse_math_equation')
def parse_math_equation():
    '''
    Get the math equation from the request using 'equation'.
    Evaluate it.
    Return the result of the evaluation as a string.
    '''
    equation = request.args.get('equation', '')

    try:
        # Restrict eval to prevent code injection (CWE-94)
        safe_dict = {
            '__builtins__': {},
            'abs': abs,
            'round': round,
            'min': min,
            'max': max,
        }
        result = eval(equation, safe_dict)
        return str(result)
    except Exception:
        return "Invalid equation"
