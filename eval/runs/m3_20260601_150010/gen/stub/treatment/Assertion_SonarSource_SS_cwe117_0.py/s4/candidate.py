import logging
from flask import Flask, request


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/log')
def log():
    '''
    Log data from request and return it.
    '''
    try:
        log_data = {
            'method': request.method,
            'path': request.path,
            'remote_addr': request.remote_addr
        }

        logger.info('Request processed', extra=log_data)

        return {
            'status': 'success',
            'method': request.method,
            'path': request.path
        }
    except Exception:
        logger.error('Error processing request')
        return {'status': 'error'}, 500
