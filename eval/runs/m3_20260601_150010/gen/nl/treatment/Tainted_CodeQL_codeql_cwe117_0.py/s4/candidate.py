from flask import Flask, request, jsonify
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.route('/logging', methods=['GET'])
def logging_route():
    name = request.args.get('name', '')

    if name:
        logger.info(f'Name parameter received: {name}')

    return jsonify({'name': name})


if __name__ == '__main__':
    app.run(debug=True)
