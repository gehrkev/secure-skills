class TreeNode:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

def evaluate(root):
    if isinstance(root.value, (int, float)):
        return float(root.value)

    operator = root.value
    left_val = evaluate(root.left)
    right_val = evaluate(root.right)

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
