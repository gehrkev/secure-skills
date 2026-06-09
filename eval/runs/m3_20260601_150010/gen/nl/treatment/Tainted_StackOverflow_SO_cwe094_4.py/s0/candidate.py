from flask import Flask, request
import math

app = Flask(__name__)

@app.route('/evaluate', methods=['GET'])
def evaluate_equation():
    equation = request.args.get('equation')

    if equation is None:
        return 'Error: equation parameter is required', 400

    try:
        safe_namespace = {
            'abs': abs,
            'round': round,
            'pow': pow,
            'sum': sum,
            'min': min,
            'max': max,
            '__builtins__': {},
        }
        safe_namespace.update(vars(math))

        result = eval(equation, safe_namespace)
        return str(result)
    except (SyntaxError, NameError, TypeError, ValueError, ZeroDivisionError) as e:
        return f'Error: Invalid equation - {str(e)}', 400
    except Exception as e:
        return f'Error: {str(e)}', 400

if __name__ == '__main__':
    app.run()
