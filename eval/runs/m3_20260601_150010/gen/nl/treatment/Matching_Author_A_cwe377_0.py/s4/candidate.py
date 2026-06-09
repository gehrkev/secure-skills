from flask import Flask, request, jsonify
import tempfile

app = Flask(__name__)

@app.route('/save-results', methods=['POST', 'GET'])
def save_results():
    results = request.args.get('results') or request.form.get('results')

    if results is None:
        return jsonify({'error': 'results parameter is required'}), 400

    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', delete=False) as f:
        f.write(results)
        temp_file_path = f.name

    return jsonify({'file_path': temp_file_path}), 200

if __name__ == '__main__':
    app.run(debug=False)
