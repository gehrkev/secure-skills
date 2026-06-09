from flask import Flask, request
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/logging')
def logging_route():
    name = request.args.get('name')
    if name:
        logger.info(f"Name: {name}")
    return name

if __name__ == '__main__':
    app.run()
