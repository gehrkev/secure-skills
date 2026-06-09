from flask import Flask, request
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/logging', methods=['GET', 'POST'])
def logging_route():
    name = request.args.get('name') or request.form.get('name')
    logger.info(f"Name parameter: {name}")
    return name or "No name provided"

if __name__ == '__main__':
    app.run()
