from flask import Flask, request
import pickle
import io

app = Flask(__name__)

class RestrictedUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        # Allowlist of safe built-in types
        if module == 'builtins' and name in ['dict', 'list', 'tuple', 'str', 'int', 'float', 'bool', 'bytes', 'frozenset', 'set', 'None']:
            return super().find_class(module, name)
        raise pickle.UnpicklingError(f"Global '{module}.{name}' is not allowed")

@app.route('/unpickled', methods=['GET', 'POST'])
def unpickled():
    data_hex = request.args.get('data') or request.form.get('data')

    if not data_hex:
        return {'error': 'data parameter required'}, 400

    try:
        data_bytes = bytes.fromhex(data_hex)
        obj = RestrictedUnpickler(io.BytesIO(data_bytes)).load()
        return {'result': obj}
    except ValueError:
        return {'error': 'Invalid hex string'}, 400
    except pickle.UnpicklingError as e:
        return {'error': str(e)}, 400
    except Exception as e:
        return {'error': str(e)}, 400

if __name__ == '__main__':
    app.run()
