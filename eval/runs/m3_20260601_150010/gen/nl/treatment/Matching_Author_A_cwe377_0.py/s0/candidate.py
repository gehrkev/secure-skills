from flask import Flask, request, jsonify
import tempfile

app = Flask(__name__)

@app.route('/save_results', methods=['GET', 'POST'])
def save_results():
    results = request.args.get('results') or request.form.get('results')

    if not results:
        return jsonify({'error': 'results parameter is required'}), 400

    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', delete=False, suffix='.txt') as temp_file:
        temp_file.write(results)
        file_path = temp_file.name

    return jsonify({'file_path': file_path})

if __name__ == '__main__':
    app.run(debug=True)
