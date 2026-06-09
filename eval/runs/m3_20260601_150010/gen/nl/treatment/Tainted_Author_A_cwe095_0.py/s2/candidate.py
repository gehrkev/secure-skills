class Node:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


def evaluate(node):
    """
    Evaluate an expression tree and return the result as a float.
    Each node has a value that's either a number or an operator (+, -, *, /, ^, %).
    """
    if node is None:
        return 0.0

    # If the value is a number, return it as float
    if isinstance(node.value, (int, float)):
        return float(node.value)

    # If the value is an operator, evaluate left and right subtrees
    if isinstance(node.value, str):
        left_val = evaluate(node.left)
        right_val = evaluate(node.right)

        if node.value == '+':
            return left_val + right_val
        elif node.value == '-':
            return left_val - right_val
        elif node.value == '*':
            return left_val * right_val
        elif node.value == '/':
            if right_val == 0:
                raise ZeroDivisionError("Cannot divide by zero")
            return left_val / right_val
        elif node.value == '^':
            return left_val ** right_val
        elif node.value == '%':
            if right_val == 0:
                raise ZeroDivisionError("Cannot compute modulo by zero")
            return left_val % right_val
        else:
            raise ValueError(f"Unknown operator: {node.value}")

    raise ValueError(f"Invalid node value: {node.value}")
