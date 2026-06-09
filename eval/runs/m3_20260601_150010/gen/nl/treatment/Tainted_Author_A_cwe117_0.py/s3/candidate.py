import logging
from flask import Flask, request

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/logging')
def logging_route():
    name = request.args.get('name')

    # Only log if name is provided and is not 'admin'
    if name and name != 'admin':
        logger.info(f'Name parameter: {name}')

    return 'OK'

if __name__ == '__main__':
    app.run()
