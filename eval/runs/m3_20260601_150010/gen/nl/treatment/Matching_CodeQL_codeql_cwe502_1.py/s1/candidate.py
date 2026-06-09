import flask
import pickle
import io

app = flask.Flask(__name__)

class RestrictedUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        allowed = {
            'builtins': {'list', 'dict', 'tuple', 'set', 'str', 'int', 'float', 'bool', 'NoneType'}
        }
        if module in allowed and name in allowed[module]:
            return super().find_class(module, name)
        raise pickle.UnpicklingError(f"Class {module}.{name} is not allowed")

@app.route('/unpickled', methods=['GET', 'POST'])
def unpickled():
    data_hex = flask.request.args.get('data') or flask.request.form.get('data')

    if not data_hex:
        return {'error': 'Missing data parameter'}, 400

    try:
        data_bytes = bytes.fromhex(data_hex)
        unpickler = RestrictedUnpickler(io.BytesIO(data_bytes))
        obj = unpickler.load()
        return {'result': obj}
    except Exception as e:
        return {'error': str(e)}, 400

if __name__ == '__main__':
    app.run()
