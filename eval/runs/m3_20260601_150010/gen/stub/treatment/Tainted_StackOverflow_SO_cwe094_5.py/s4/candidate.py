from flask import Flask, request
import json


app = Flask(__name__)

class Tree(object):
    '''
    A tree.
    '''

    def __init__(self, root):
        '''
        Initialize the tree.

        :param root: The root node.
        '''

        self.root = root

    def get_root(self):
        '''
        Get the root node.

        :return: The root node.
        '''

        return self.root

@app.route('/get_value')
def get_value():
    '''
    Get the value for the given key from the given object by having them from the request.
    Return the value as a string.
    '''
    key = request.args.get('key')
    obj_data = request.args.get('obj')

    if key is None or obj_data is None:
        return ""

    try:
        obj = json.loads(obj_data)
        value = obj.get(key) if isinstance(obj, dict) else None
        return str(value) if value is not None else ""
    except (json.JSONDecodeError, AttributeError, TypeError):
        return ""
