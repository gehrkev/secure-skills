import logging
from flask import Flask, request


app = Flask(__name__)

@app.route('/log')
def log():
    '''
    Log data from request and return it.
    '''
    data = {
        'method': request.method,
        'path': request.path,
        'query_string': request.query_string.decode('utf-8') if request.query_string else None,
        'json': request.get_json() if request.is_json else None,
    }

    logging.info(f"Request data: {data}")

    return data
