import pickle
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/load_config')
def load_config():
    config = request.args.get('config')
    if not config:
        return jsonify({'error': 'Missing config parameter'}), 400

    try:
        config_bytes = bytes.fromhex(config)
        config_data = pickle.loads(config_bytes)
        return jsonify({'config': config_data}), 200
    except ValueError:
        return jsonify({'error': 'Invalid hex encoding'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=False)
