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
    data = {
        'method': request.method,
        'path': request.path,
        'args': dict(request.args),
        'headers': dict(request.headers),
    }
    logger.info(f"Request data: {data}")
    return data
