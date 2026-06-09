import flask
import pickle
import io

app = flask.Flask(__name__)

class RestrictedUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        safe_classes = {
            'builtins.int',
            'builtins.str',
            'builtins.list',
            'builtins.dict',
            'builtins.tuple',
            'builtins.bool',
            'builtins.float',
            'builtins.bytes',
        }

        full_name = f"{module}.{name}"
        if full_name not in safe_classes:
            raise pickle.UnpicklingError(f"Class {full_name} is not allowed for deserialization")

        return super().find_class(module, name)

@app.route('/unpickled')
def unpickled():
    data = flask.request.args.get('data')
    if not data:
        return {'error': 'Missing data parameter'}, 400

    try:
        pickled_bytes = bytes.fromhex(data)
        obj = RestrictedUnpickler(io.BytesIO(pickled_bytes)).load()
        return obj
    except ValueError:
        return {'error': 'Invalid hex data'}, 400
    except pickle.UnpicklingError as e:
        return {'error': str(e)}, 400

if __name__ == '__main__':
    app.run()
