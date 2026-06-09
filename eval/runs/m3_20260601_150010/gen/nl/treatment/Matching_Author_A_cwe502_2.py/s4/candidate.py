from flask import Flask, request, jsonify
import pickle
import binascii
import io

app = Flask(__name__)

class RestrictedUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        # Allowlist of safe classes to prevent arbitrary code execution
        allowed_classes = {
            ('builtins', 'dict'),
            ('builtins', 'list'),
            ('builtins', 'tuple'),
            ('builtins', 'set'),
            ('builtins', 'str'),
            ('builtins', 'int'),
            ('builtins', 'float'),
            ('builtins', 'bool'),
            ('builtins', 'bytes'),
            ('builtins', 'bytearray'),
            ('builtins', 'frozenset'),
        }
        if (module, name) not in allowed_classes:
            raise pickle.UnpicklingError(f"Class '{module}.{name}' is not allowed")
        return super().find_class(module, name)

@app.route('/unpickled', methods=['GET', 'POST'])
def unpickled():
    try:
        # Get data from request parameter
        data_hex = request.args.get('data') or request.form.get('data')
        if not data_hex:
            return jsonify({'error': 'Missing data parameter'}), 400

        # Convert hex to bytes
        data_bytes = binascii.unhexlify(data_hex)

        # Unpickle with restricted unpickler
        deserialized = RestrictedUnpickler(io.BytesIO(data_bytes)).load()

        return jsonify({'result': deserialized})
    except binascii.Error:
        return jsonify({'error': 'Invalid hex data'}), 400
    except pickle.UnpicklingError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Deserialization failed'}), 400

if __name__ == '__main__':
    app.run()
