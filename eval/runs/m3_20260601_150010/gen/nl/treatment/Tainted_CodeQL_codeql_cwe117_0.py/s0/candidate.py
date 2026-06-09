from flask import Flask, request
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/logging', methods=['GET', 'POST'])
def logging_route():
    name = request.args.get('name') or request.form.get('name')
    if name:
        logger.info(f"Name received: {name}")
    return {'name': name}

if __name__ == '__main__':
    app.run()
