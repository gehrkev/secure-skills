from flask import Flask, request
import tempfile

app = Flask(__name__)

@app.route('/save', methods=['GET', 'POST'])
def save_results():
    results = request.args.get('results') or request.form.get('results')

    if not results:
        return {'error': 'results parameter is required'}, 400

    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', delete=False) as f:
        f.write(results)
        temp_file_path = f.name

    return {'file_path': temp_file_path}

if __name__ == '__main__':
    app.run()
