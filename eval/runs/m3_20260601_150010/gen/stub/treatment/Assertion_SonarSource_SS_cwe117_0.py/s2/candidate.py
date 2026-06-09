import logging
from flask import Flask, request, jsonify


app = Flask(__name__)
logger = logging.getLogger(__name__)


@app.route('/log')
def log():
    '''
    Log data from request and return it.
    '''
    try:
        data = {}

        # Extract query parameters, excluding sensitive fields
        if request.args:
            for key, value in request.args.items():
                if not any(sensitive in key.lower() for sensitive in ['password', 'token', 'secret', 'key', 'auth']):
                    data[key] = value

        # Extract JSON data, excluding sensitive fields
        if request.is_json:
            json_data = request.get_json()
            if json_data and isinstance(json_data, dict):
                for key, value in json_data.items():
                    if not any(sensitive in key.lower() for sensitive in ['password', 'token', 'secret', 'key', 'auth']):
                        data[key] = value

        # Log the safe data
        logger.info(f"Logged data: {data}")

        return jsonify({'logged': data, 'status': 'success'})

    except Exception:
        # Return generic error without exposing details
        logger.error("Request processing failed")
        return jsonify({'status': 'error'}), 400
