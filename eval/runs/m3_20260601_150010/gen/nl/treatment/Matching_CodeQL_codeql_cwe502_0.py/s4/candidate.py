import flask
import pickle
from io import BytesIO

app = flask.Flask(__name__)

class RestrictedUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        allowed = {
            ('builtins', 'dict'),
            ('builtins', 'list'),
            ('builtins', 'tuple'),
            ('builtins', 'set'),
            ('builtins', 'str'),
            ('builtins', 'int'),
            ('builtins', 'float'),
            ('builtins', 'bool'),
            ('builtins', 'NoneType'),
        }
        if (module, name) not in allowed:
            raise pickle.UnpicklingError(f"Class {module}.{name} is not allowed")
        return super().find_class(module, name)

def to_json_serializable(obj):
    if isinstance(obj, dict):
        return {k: to_json_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [to_json_serializable(item) for item in obj]
    elif isinstance(obj, tuple):
        return [to_json_serializable(item) for item in obj]
    elif isinstance(obj, set):
        return [to_json_serializable(item) for item in obj]
    else:
        return obj

@app.route('/unpickled_data', methods=['POST', 'GET'])
def unpickled_data():
    data_hex = flask.request.args.get('data') or flask.request.form.get('data')

    if not data_hex:
        return {'error': 'Missing data parameter'}, 400

    try:
        data_bytes = bytes.fromhex(data_hex)
        unpickler = RestrictedUnpickler(BytesIO(data_bytes))
        result = unpickler.load()
        return to_json_serializable(result)
    except ValueError:
        return {'error': 'Invalid hex data'}, 400
    except pickle.UnpicklingError as e:
        return {'error': str(e)}, 400

if __name__ == '__main__':
    app.run()
