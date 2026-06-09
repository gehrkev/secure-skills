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
    obj_str = request.args.get('obj')

    if not key or not obj_str:
        return ''

    try:
        obj = json.loads(obj_str)
        if isinstance(obj, dict):
            value = obj.get(key)
        else:
            value = getattr(obj, key, None)
        return str(value) if value is not None else ''
    except (json.JSONDecodeError, AttributeError, TypeError):
        return ''
