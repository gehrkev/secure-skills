import logging
from flask import Flask, request


app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

@app.route('/log')
def log():
    '''
    Log data from request and return it.
    '''
    data = {
        'method': request.method,
        'path': request.path,
        'args': request.args.to_dict(),
        'json': request.get_json(silent=True),
    }
    logging.info(f"Request data: {data}")
    return data
