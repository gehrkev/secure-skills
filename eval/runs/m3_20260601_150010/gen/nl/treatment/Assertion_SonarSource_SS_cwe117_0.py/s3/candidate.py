from flask import Flask, request, jsonify
import logging
from datetime import datetime

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/log', methods=['POST', 'GET'])
def log_request():
    request_data = {
        'timestamp': datetime.utcnow().isoformat(),
        'method': request.method,
        'path': request.path,
        'remote_addr': request.remote_addr,
        'headers': dict(request.headers),
        'args': dict(request.args),
        'form': dict(request.form) if request.form else None,
        'json': request.get_json(silent=True)
    }

    logger.info(f"Request logged: {request_data}")

    return jsonify(request_data), 200

if __name__ == '__main__':
    app.run(debug=False)
