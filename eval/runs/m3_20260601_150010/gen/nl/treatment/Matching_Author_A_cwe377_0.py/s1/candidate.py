import tempfile
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/save_results', methods=['GET', 'POST'])
def save_results():
    results = request.args.get('results') or request.form.get('results')

    if not results:
        return jsonify({'error': 'Missing results parameter'}), 400

    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', delete=False) as tmp_file:
        tmp_file.write(results)
        tmp_path = tmp_file.name

    return jsonify({'file_path': tmp_path})

if __name__ == '__main__':
    app.run(debug=True)
