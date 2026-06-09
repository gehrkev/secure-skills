class TreeNode:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

def evaluate_tree(node):
    if node is None:
        return 0.0

    if isinstance(node.value, (int, float)):
        return float(node.value)

    operator = node.value
    left_val = evaluate_tree(node.left)
    right_val = evaluate_tree(node.right)

    if operator == '+':
        return left_val + right_val
    elif operator == '-':
        return left_val - right_val
    elif operator == '*':
        return left_val * right_val
    elif operator == '/':
        if right_val == 0:
            raise ValueError("Division by zero")
        return left_val / right_val
    elif operator == '^':
        return left_val ** right_val
    elif operator == '%':
        if right_val == 0:
            raise ValueError("Modulo by zero")
        return left_val % right_val
    else:
        raise ValueError(f"Unknown operator: {operator}")
