from flask import Flask, request, jsonify
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/logging', methods=['GET', 'POST'])
def log_name():
    name = request.args.get('name')
    if not name and request.method == 'POST':
        if request.is_json:
            name = request.json.get('name')
        else:
            name = request.form.get('name')

    if not name:
        return jsonify({'error': 'Name parameter required'}), 400

    logger.info(f"Name: {name}")
    return jsonify({'name': name})

if __name__ == '__main__':
    app.run(debug=True)
