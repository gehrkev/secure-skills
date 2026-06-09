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
    data = {
        'method': request.method,
        'path': request.path,
        'remote_addr': request.remote_addr,
    }

    logger.info(f"Request: {data}")

    return data
