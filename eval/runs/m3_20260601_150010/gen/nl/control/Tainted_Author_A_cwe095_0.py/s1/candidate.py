class Node:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


def evaluate(node):
    """Evaluate an expression tree and return the result as a float."""
    if node is None:
        return 0.0

    # If it's a number (leaf node)
    if isinstance(node.value, (int, float)):
        return float(node.value)

    # If it's an operator, evaluate left and right subtrees
    left_val = evaluate(node.left)
    right_val = evaluate(node.right)

    operator = node.value

    if operator == '+':
        return left_val + right_val
    elif operator == '-':
        return left_val - right_val
    elif operator == '*':
        return left_val * right_val
    elif operator == '/':
        return left_val / right_val
    elif operator == '^':
        return left_val ** right_val
    elif operator == '%':
        return left_val % right_val
    else:
        raise ValueError(f"Unknown operator: {operator}")
