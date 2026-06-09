from flask import Flask, request, jsonify
import tempfile

app = Flask(__name__)

@app.route('/save_results', methods=['POST', 'GET'])
def save_results():
    results = request.form.get('results') or request.args.get('results')

    if not results:
        return jsonify({'error': 'results parameter is required'}), 400

    try:
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', delete=False, suffix='.txt') as temp_file:
            temp_file.write(results)
            file_path = temp_file.name

        return jsonify({'file_path': file_path}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run()
