import flask
import pickle
import io

app = flask.Flask(__name__)

class RestrictedUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        if module == "builtins" and name in {"int", "str", "float", "list", "dict", "tuple", "set", "frozenset", "bytes", "bool"}:
            return super().find_class(module, name)
        raise pickle.UnpicklingError(f"Deserialization of {module}.{name} not allowed")

@app.route('/unpickled', methods=['GET', 'POST'])
def unpickled():
    data_hex = flask.request.args.get('data') or flask.request.form.get('data')
    if not data_hex:
        return {"error": "Missing 'data' parameter"}, 400

    try:
        data_bytes = bytes.fromhex(data_hex)
        unpickler = RestrictedUnpickler(io.BytesIO(data_bytes))
        result = unpickler.load()
        return {"result": result}
    except ValueError:
        return {"error": "Invalid hex data"}, 400
    except pickle.UnpicklingError as e:
        return {"error": str(e)}, 400
