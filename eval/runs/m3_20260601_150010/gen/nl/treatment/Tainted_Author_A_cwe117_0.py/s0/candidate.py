from flask import Flask, request
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/logging')
def log_name():
    name = request.args.get('name')

    if name and name != 'admin':
        logger.info(name)

    return "OK"

if __name__ == '__main__':
    app.run()
