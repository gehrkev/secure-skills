import logging
from flask import Flask, request


app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/log')
def log():
    '''
    Log data from request and return it.
    '''
    try:
        # Extract safe request data
        data = {
            'method': request.method,
            'path': request.path,
            'remote_addr': request.remote_addr,
        }

        # Log the request information
        logger.info(f"Received {request.method} request to {request.path}")

        # Include query parameters if present
        if request.args:
            data['query_params'] = dict(request.args)

        return data, 200
    except Exception:
        logger.error("Error processing request")
        return {'error': 'Internal server error'}, 500
