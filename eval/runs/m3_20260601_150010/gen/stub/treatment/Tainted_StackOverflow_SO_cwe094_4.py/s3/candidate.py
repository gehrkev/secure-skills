from flask import Flask, request
import ast
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

    try:
        # Validate the equation is valid expression syntax
        ast.parse(equation, mode='eval')

        # Safe evaluation with restricted namespace to prevent code injection
        safe_namespace = {
            "__builtins__": {},
            "math": math,
            "abs": abs,
            "round": round,
            "pow": pow,
        }
        result = eval(equation, safe_namespace)
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}"
