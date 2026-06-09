class Node:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


def evaluate_expression_tree(root):
    """
    Evaluate an expression tree and return the result as a float.

    Each node has a value that's either a number or an operator (+, -, *, /, ^, %).
    Traverse the tree recursively and compute the result.
    """
    if root is None:
        return 0.0

    # Base case: leaf node with a number
    if isinstance(root.value, (int, float)):
        return float(root.value)

    # Recursive case: node with an operator
    left_result = evaluate_expression_tree(root.left)
    right_result = evaluate_expression_tree(root.right)

    operator = root.value

    if operator == '+':
        return left_result + right_result
    elif operator == '-':
        return left_result - right_result
    elif operator == '*':
        return left_result * right_result
    elif operator == '/':
        return left_result / right_result
    elif operator == '^':
        return left_result ** right_result
    elif operator == '%':
        return left_result % right_result
    else:
        raise ValueError(f"Unknown operator: {operator}")
