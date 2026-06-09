class Node:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


def evaluate_tree(root):
    """
    Evaluate an expression tree and return the result as a float.

    Each node has a value that's either a number or an operator (+, -, *, /, ^, %).
    Numeric nodes are leaves; operator nodes have left and right subtrees.
    """
    if root is None:
        return 0.0

    # Leaf node: numeric value
    if isinstance(root.value, (int, float)):
        return float(root.value)

    # Operator node: recursively evaluate operands
    left_val = evaluate_tree(root.left)
    right_val = evaluate_tree(root.right)

    op = root.value

    if op == '+':
        return left_val + right_val
    elif op == '-':
        return left_val - right_val
    elif op == '*':
        return left_val * right_val
    elif op == '/':
        if right_val == 0:
            raise ValueError("Division by zero")
        return left_val / right_val
    elif op == '^':
        return left_val ** right_val
    elif op == '%':
        if right_val == 0:
            raise ValueError("Modulo by zero")
        return left_val % right_val
    else:
        raise ValueError(f"Unknown operator: {op}")
