from flask import Flask, request, jsonify
import logging
from datetime import datetime

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.route('/log', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
def log_request():
    """Log incoming request data and return it."""
    request_data = {
        'timestamp': datetime.utcnow().isoformat(),
        'method': request.method,
        'path': request.path,
        'remote_addr': request.remote_addr,
        'headers': dict(request.headers),
        'args': dict(request.args),
    }

    if request.method in ['POST', 'PUT', 'PATCH']:
        if request.is_json:
            request_data['json'] = request.get_json()
        else:
            request_data['form'] = dict(request.form)

    logger.info(f"Logged request: {request_data}")

    return jsonify(request_data), 200


if __name__ == '__main__':
    app.run(debug=False)
