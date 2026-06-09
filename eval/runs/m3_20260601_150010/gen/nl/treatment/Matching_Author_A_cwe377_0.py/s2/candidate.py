import flask
import tempfile

app = flask.Flask(__name__)

@app.route('/write_results', methods=['POST', 'GET'])
def write_results():
    results = flask.request.args.get('results', '') or flask.request.form.get('results', '')

    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', delete=False) as tmp_file:
        tmp_file.write(results)
        temp_file_path = tmp_file.name

    return {'file_path': temp_file_path}

if __name__ == '__main__':
    app.run(debug=True)
