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
    data = request.get_json() or request.args.to_dict() or {}
    logger.info(f"Request data: {data}")
    return jsonify(data)
