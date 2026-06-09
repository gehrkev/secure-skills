class Node:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


def evaluate(node):
    if isinstance(node.value, (int, float)):
        return float(node.value)

    left_val = evaluate(node.left)
    right_val = evaluate(node.right)

    if node.value == '+':
        return left_val + right_val
    elif node.value == '-':
        return left_val - right_val
    elif node.value == '*':
        return left_val * right_val
    elif node.value == '/':
        return left_val / right_val
    elif node.value == '^':
        return left_val ** right_val
    elif node.value == '%':
        return left_val % right_val
