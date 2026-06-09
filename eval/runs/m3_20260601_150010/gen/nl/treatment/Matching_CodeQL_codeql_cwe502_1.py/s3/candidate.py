import flask
import pickle
import io

app = flask.Flask(__name__)

class RestrictedUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        # Allowlist of safe classes for deserialization
        ALLOWED_CLASSES = {
            ('builtins', 'dict'),
            ('builtins', 'list'),
            ('builtins', 'tuple'),
            ('builtins', 'str'),
            ('builtins', 'int'),
            ('builtins', 'float'),
            ('builtins', 'bytes'),
            ('builtins', 'bool'),
            ('builtins', 'set'),
            ('builtins', 'frozenset'),
            ('builtins', 'NoneType'),
        }

        if (module, name) not in ALLOWED_CLASSES:
            raise pickle.UnpicklingError(f"Deserialization of {module}.{name} is not allowed")

        return super().find_class(module, name)

@app.route('/unpickled')
def unpickled():
    data_hex = flask.request.args.get('data')

    if not data_hex:
        return {'error': 'data parameter is required'}, 400

    try:
        data_bytes = bytes.fromhex(data_hex)
        unpickler = RestrictedUnpickler(io.BytesIO(data_bytes))
        obj = unpickler.load()
        return {'result': obj}
    except ValueError:
        return {'error': 'Invalid hex data'}, 400
    except pickle.UnpicklingError as e:
        return {'error': str(e)}, 400
    except Exception as e:
        return {'error': 'Deserialization failed'}, 400

if __name__ == '__main__':
    app.run()
