from flask import Flask, request
import math
import ast

app = Flask(__name__)

def is_safe_equation(equation):
    """Verify that the equation only contains safe AST nodes"""
    try:
        tree = ast.parse(equation, mode='eval')
        allowed_nodes = (
            ast.Expression, ast.BinOp, ast.UnaryOp, ast.Constant,
            ast.Name, ast.Call, ast.Attribute
        )
        for node in ast.walk(tree):
            if not isinstance(node, allowed_nodes):
                return False
        return True
    except:
        return False

@app.route('/evaluate', methods=['GET', 'POST'])
def evaluate():
    equation = request.args.get('equation', '')

    if not equation:
        return "Missing equation parameter"

    if not is_safe_equation(equation):
        return "Invalid equation"

    try:
        safe_namespace = {name: getattr(math, name) for name in dir(math) if not name.startswith('_')}
        safe_namespace['__builtins__'] = {}

        result = eval(equation, safe_namespace)
        return str(result)
    except Exception:
        return "Error evaluating equation"

if __name__ == '__main__':
    app.run()
