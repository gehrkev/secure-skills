import logging
from flask import Flask, request, jsonify

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/log')
def log():
    '''
    Log data from request and return it.
    '''
    try:
        data = {}

        if request.args:
            data['query_params'] = dict(request.args)

        if request.method == 'POST' and request.is_json:
            data['json_body'] = request.get_json()

        if request.headers:
            safe_headers = {k: v for k, v in request.headers if k.lower() not in ['authorization', 'cookie', 'x-api-key']}
            if safe_headers:
                data['headers'] = dict(safe_headers)

        data['method'] = request.method
        data['path'] = request.path

        logger.info('Request data: %s', data)

        return jsonify({'received': data}), 200

    except Exception as e:
        logger.error('Error processing request')
        return jsonify({'error': 'Unable to process request'}), 400
