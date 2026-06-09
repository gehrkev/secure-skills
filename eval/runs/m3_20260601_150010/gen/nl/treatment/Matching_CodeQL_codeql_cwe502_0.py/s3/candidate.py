from flask import Flask, request
import pickle
import io

app = Flask(__name__)

class RestrictedUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        allowed_classes = {
            ('builtins', 'dict'),
            ('builtins', 'list'),
            ('builtins', 'tuple'),
            ('builtins', 'set'),
            ('builtins', 'frozenset'),
            ('builtins', 'str'),
            ('builtins', 'int'),
            ('builtins', 'float'),
            ('builtins', 'bool'),
            ('builtins', 'bytes'),
            ('builtins', 'bytearray'),
            ('builtins', 'complex'),
            ('builtins', 'range'),
            ('builtins', 'slice'),
            ('builtins', 'type'),
            ('builtins', 'object'),
        }

        if (module, name) not in allowed_classes:
            raise pickle.UnpicklingError(f"Deserialization of {module}.{name} is not allowed")

        return super().find_class(module, name)

@app.route('/unpickled_data', methods=['GET', 'POST'])
def unpickled_data():
    hex_data = request.args.get('data') or request.form.get('data')

    if not hex_data:
        try:
            json_data = request.get_json()
            hex_data = json_data.get('data') if json_data else None
        except Exception:
            pass

    if not hex_data:
        return {'error': 'No data provided'}, 400

    try:
        data_bytes = bytes.fromhex(hex_data)
        unpickler = RestrictedUnpickler(io.BytesIO(data_bytes))
        unpickled_obj = unpickler.load()
        return unpickled_obj
    except ValueError as e:
        return {'error': f'Invalid hex data: {str(e)}'}, 400
    except pickle.UnpicklingError as e:
        return {'error': f'Deserialization error: {str(e)}'}, 400
