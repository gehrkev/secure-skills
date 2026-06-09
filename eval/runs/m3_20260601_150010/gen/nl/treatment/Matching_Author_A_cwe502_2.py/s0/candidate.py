from flask import Flask, request, jsonify
import pickle
import io

app = Flask(__name__)

class SafeUnpickler(pickle.Unpickler):
    """Unpickler that restricts deserialization to safe built-in types."""

    ALLOWED_MODULES = frozenset(['builtins', '__builtins__'])
    ALLOWED_CLASSES = frozenset([
        'dict', 'list', 'tuple', 'set', 'frozenset',
        'str', 'bytes', 'bytearray',
        'int', 'float', 'complex', 'bool', 'NoneType',
        'range', 'slice'
    ])

    def find_class(self, module, name):
        if module not in self.ALLOWED_MODULES or name not in self.ALLOWED_CLASSES:
            raise pickle.UnpicklingError(
                f"Deserialization of {module}.{name} is not allowed"
            )
        return super().find_class(module, name)

@app.route('/unpickled', methods=['GET', 'POST'])
def unpickled():
    data_hex = request.args.get('data') or request.form.get('data')

    if not data_hex:
        return jsonify({'error': 'Missing data parameter'}), 400

    try:
        data_bytes = bytes.fromhex(data_hex)
        deserialized = SafeUnpickler(io.BytesIO(data_bytes)).load()
        return jsonify({'result': deserialized})
    except ValueError as e:
        return jsonify({'error': f'Invalid hex data: {str(e)}'}), 400
    except pickle.UnpicklingError as e:
        return jsonify({'error': f'Unpickling error: {str(e)}'}), 400

if __name__ == '__main__':
    app.run(debug=True)
