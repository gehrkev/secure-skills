from flask import Flask, request
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/logging')
def logging_route():
    name = request.args.get('name')
    logger.info(f"Received name: {name}")
    return name
