import pickle
import io
from flask import Flask, request, jsonify

app = Flask(__name__)

class SafeUnpickler(pickle.Unpickler):
    """Unpickler that restricts deserialization to safe built-in types"""

    ALLOWED_MODULES = {'builtins'}
    ALLOWED_NAMES = {
        'dict', 'list', 'tuple', 'set', 'frozenset',
        'str', 'bytes', 'bytearray',
        'int', 'float', 'complex',
        'bool', 'NoneType',
        'type',
    }

    def find_class(self, module, name):
        if module not in self.ALLOWED_MODULES:
            raise pickle.UnpicklingError(f"Module '{module}' not allowed")
        if name not in self.ALLOWED_NAMES:
            raise pickle.UnpicklingError(f"Type '{name}' not allowed")
        return super().find_class(module, name)

@app.route('/unpickled', methods=['GET'])
def unpickled():
    try:
        hex_data = request.args.get('data')
        if not hex_data:
            return jsonify({'error': 'Missing data parameter'}), 400

        # Convert hex to bytes
        pickled_bytes = bytes.fromhex(hex_data)

        # Unpickle with class restrictions
        unpickler = SafeUnpickler(io.BytesIO(pickled_bytes))
        data = unpickler.load()

        return jsonify({'data': data})

    except ValueError:
        return jsonify({'error': 'Invalid hex encoding'}), 400
    except pickle.UnpicklingError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Deserialization failed'}), 400

if __name__ == '__main__':
    app.run(debug=False)
