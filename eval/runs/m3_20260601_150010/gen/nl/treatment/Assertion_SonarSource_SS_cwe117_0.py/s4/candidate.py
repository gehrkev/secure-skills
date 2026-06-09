from flask import Flask, request, jsonify
import logging
from datetime import datetime

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SENSITIVE_HEADERS = {'authorization', 'cookie', 'set-cookie', 'x-api-key', 'x-auth-token'}

@app.route('/log', methods=['GET', 'POST'])
def log_request():
    """Log incoming request data and return it."""

    headers = {}
    for key, value in request.headers:
        if key.lower() not in SENSITIVE_HEADERS:
            headers[key] = value

    request_data = {
        'timestamp': datetime.utcnow().isoformat(),
        'method': request.method,
        'path': request.path,
        'remote_addr': request.remote_addr,
        'headers': headers,
        'args': dict(request.args),
        'form': dict(request.form) if request.form else {},
        'json': request.get_json(silent=True),
    }

    logger.info(f"Request logged: {request_data}")

    return jsonify(request_data)

if __name__ == '__main__':
    app.run(debug=False)
