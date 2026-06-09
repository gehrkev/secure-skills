import logging
from flask import Flask, request, jsonify

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/logging', methods=['GET', 'POST'])
def logging_route():
    # Try to get name from GET parameters first, then POST data
    name = request.args.get('name')
    if not name and request.method == 'POST':
        if request.is_json:
            name = request.json.get('name')
        else:
            name = request.form.get('name')

    if name:
        logger.info(f"Retrieved name: {name}")
        return jsonify({'name': name})
    else:
        return jsonify({'error': 'Name parameter is required'}), 400

if __name__ == '__main__':
    app.run()
