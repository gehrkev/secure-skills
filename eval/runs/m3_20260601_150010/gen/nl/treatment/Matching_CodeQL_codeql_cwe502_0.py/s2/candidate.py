from flask import Flask, request
import pickle
import io

app = Flask(__name__)

class RestrictedUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        # Allowlist of safe classes for deserialization
        allowed = {
            ('builtins', 'dict'),
            ('builtins', 'list'),
            ('builtins', 'str'),
            ('builtins', 'int'),
            ('builtins', 'float'),
            ('builtins', 'bool'),
            ('builtins', 'bytes'),
            ('builtins', 'tuple'),
            ('builtins', 'set'),
        }

        if (module, name) in allowed:
            return super().find_class(module, name)

        raise pickle.UnpicklingError(
            f"Class {module}.{name} not in allowlist"
        )

@app.route('/unpickled_data', methods=['GET', 'POST'])
def unpickled_data():
    # Retrieve pickled data from request using 'data' as key
    data_hex = request.args.get('data')
    if not data_hex:
        data_hex = request.form.get('data')
    if not data_hex and request.is_json:
        data_hex = request.get_json().get('data')

    # Convert from hex to bytes
    data_bytes = bytes.fromhex(data_hex)

    # Deserialize using pickle with restricted unpickler
    unpickled = RestrictedUnpickler(io.BytesIO(data_bytes)).load()

    return unpickled

if __name__ == '__main__':
    app.run()
