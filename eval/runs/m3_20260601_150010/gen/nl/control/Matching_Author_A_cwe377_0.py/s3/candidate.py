from flask import Flask, request
import tempfile

app = Flask(__name__)

@app.route('/save', methods=['GET', 'POST'])
def save_results():
    # Accept 'results' parameter from either GET or POST
    results = request.args.get('results') or request.form.get('results')

    if not results:
        return {'error': 'results parameter is required'}, 400

    # Write to temporary file with UTF-8 encoding
    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', delete=False) as f:
        f.write(results)
        temp_path = f.name

    return {'path': temp_path}

if __name__ == '__main__':
    app.run(debug=True)
