from flask import Flask, request
import tempfile

app = Flask(__name__)

@app.route('/results', methods=['GET', 'POST'])
def handle_results():
    results_param = request.args.get('results') or request.form.get('results')

    if not results_param:
        return {'error': 'results parameter is required'}, 400

    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', delete=False) as temp_file:
        temp_file.write(results_param)
        temp_file_path = temp_file.name

    return {'file_path': temp_file_path}

if __name__ == '__main__':
    app.run()
