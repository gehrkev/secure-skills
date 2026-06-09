class TreeNode:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

def evaluate(root):
    if root is None:
        return 0.0

    if isinstance(root.value, (int, float)):
        return float(root.value)

    left_val = evaluate(root.left)
    right_val = evaluate(root.right)

    if root.value == '+':
        return left_val + right_val
    elif root.value == '-':
        return left_val - right_val
    elif root.value == '*':
        return left_val * right_val
    elif root.value == '/':
        if right_val == 0:
            raise ValueError("Division by zero")
        return left_val / right_val
    elif root.value == '^':
        return left_val ** right_val
    elif root.value == '%':
        if right_val == 0:
            raise ValueError("Modulo by zero")
        return left_val % right_val
    else:
        raise ValueError(f"Unknown operator: {root.value}")
