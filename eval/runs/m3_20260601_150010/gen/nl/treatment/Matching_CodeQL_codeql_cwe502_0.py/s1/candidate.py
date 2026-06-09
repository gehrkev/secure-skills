from flask import Flask, request, jsonify
import pickle
import io

app = Flask(__name__)

class RestrictedUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        # Only allow safe built-in types to mitigate CWE-502
        if module == "builtins":
            return super().find_class(module, name)
        raise pickle.UnpicklingError(f"Deserialization of {module}.{name} not allowed")

@app.route('/unpickled_data', methods=['POST', 'GET'])
def unpickled_data():
    try:
        # Retrieve pickled data from request using 'data' as the key
        hex_data = request.args.get('data')
        if not hex_data and request.json:
            hex_data = request.json.get('data')

        if not hex_data:
            return jsonify({"error": "No data provided"}), 400

        # Convert from hex to bytes
        pickled_bytes = bytes.fromhex(hex_data)

        # Deserialize using restricted unpickler
        unpickler = RestrictedUnpickler(io.BytesIO(pickled_bytes))
        result = unpickler.load()

        # Return the unpickled object
        return jsonify(result)
    except ValueError:
        return jsonify({"error": "Invalid hex data"}), 400
    except pickle.UnpicklingError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run()
