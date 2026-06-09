class Node:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


def evaluate(node):
    """
    Evaluate an expression tree and return the result as a float.

    Args:
        node: Root node of the expression tree

    Returns:
        float: The computed result of the expression
    """
    if node is None:
        return 0.0

    if isinstance(node.value, (int, float)):
        return float(node.value)

    left_val = evaluate(node.left)
    right_val = evaluate(node.right)

    op = node.value
    if op == '+':
        return left_val + right_val
    elif op == '-':
        return left_val - right_val
    elif op == '*':
        return left_val * right_val
    elif op == '/':
        return left_val / right_val
    elif op == '^':
        return left_val ** right_val
    elif op == '%':
        return left_val % right_val
    else:
        raise ValueError(f"Unknown operator: {op}")
