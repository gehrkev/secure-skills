class Node:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


def evaluate(node):
    """
    Evaluate an expression tree and return the result as a float.

    Args:
        node: Root node of the expression tree. Each node has a value that's
              either a number or an operator (+, -, *, /, ^, %).

    Returns:
        float: The result of evaluating the expression tree.

    Raises:
        ValueError: If division or modulo by zero is encountered.
    """
    if node is None:
        return 0.0

    # If the node value is a number, return it as a float
    if isinstance(node.value, (int, float)):
        return float(node.value)

    # If the node value is an operator, recursively evaluate children
    if isinstance(node.value, str) and node.value in ['+', '-', '*', '/', '^', '%']:
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
                raise ValueError("Division by zero")
            return left_val / right_val
        elif node.value == '^':
            return left_val ** right_val
        elif node.value == '%':
            if right_val == 0:
                raise ValueError("Modulo by zero")
            return left_val % right_val

    return 0.0
