from flask import Flask, request
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/logging')
def logging_route():
    name = request.args.get('name')

    if name and name != 'admin':
        logger.info(f"Logged name: {name}")

    return '', 200

if __name__ == '__main__':
    app.run()
