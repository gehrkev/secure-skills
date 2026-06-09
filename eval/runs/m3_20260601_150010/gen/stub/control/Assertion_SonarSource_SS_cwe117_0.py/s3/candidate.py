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
        'args': request.args.to_dict(),
    }

    logger.info(f"Request data: {data}")

    return data


if __name__ == '__main__':
    app.run()
