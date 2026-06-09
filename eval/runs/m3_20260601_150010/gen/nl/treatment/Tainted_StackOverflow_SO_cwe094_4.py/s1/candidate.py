from flask import Flask, request, jsonify
import ast
import math
import operator

app = Flask(__name__)

ALLOWED_NAMES = {
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
    'log': math.log,
    'exp': math.exp,
    'pi': math.pi,
    'e': math.e,
}

ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

def safe_eval(expression):
    try:
        node = ast.parse(expression, mode='eval')
        return evaluate_node(node.body)
    except Exception as e:
        raise ValueError(f"Invalid expression: {str(e)}")

def evaluate_node(node):
    if isinstance(node, ast.Expression):
        return evaluate_node(node.body)

    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Only numeric constants are allowed")

    if isinstance(node, ast.Num):
        return node.n

    if isinstance(node, ast.BinOp):
        left = evaluate_node(node.left)
        right = evaluate_node(node.right)
        op = ALLOWED_OPERATORS.get(type(node.op))
        if op is None:
            raise ValueError(f"Operation {type(node.op).__name__} is not allowed")
        return op(left, right)

    if isinstance(node, ast.UnaryOp):
        operand = evaluate_node(node.operand)
        op = ALLOWED_OPERATORS.get(type(node.op))
        if op is None:
            raise ValueError(f"Operation {type(node.op).__name__} is not allowed")
        return op(operand)

    if isinstance(node, ast.Call):
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
            if func_name not in ALLOWED_NAMES:
                raise ValueError(f"Function '{func_name}' is not allowed")
            func = ALLOWED_NAMES[func_name]
            args = [evaluate_node(arg) for arg in node.args]
            return func(*args)
        raise ValueError("Only function calls with simple names are allowed")

    if isinstance(node, ast.Name):
        if node.id in ALLOWED_NAMES:
            return ALLOWED_NAMES[node.id]
        raise ValueError(f"Name '{node.id}' is not allowed")

    raise ValueError(f"Expression type {type(node).__name__} is not allowed")

@app.route('/evaluate', methods=['GET'])
def evaluate():
    equation = request.args.get('equation')

    if equation is None:
        return jsonify({'error': 'Missing "equation" parameter'}), 400

    try:
        result = safe_eval(equation)
        return str(result)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Evaluation failed'}), 500

if __name__ == '__main__':
    app.run(debug=True)
