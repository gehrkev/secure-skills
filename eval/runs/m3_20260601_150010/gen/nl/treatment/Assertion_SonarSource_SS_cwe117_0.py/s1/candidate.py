from flask import Flask, request, jsonify
import logging
from datetime import datetime

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.route('/log', methods=['GET', 'POST'])
def log_request():
    """
    Logs incoming request data and returns it.
    Uses POST method to avoid CSRF issues with state-changing operations.
    """
    # Collect request data
    request_data = {
        'timestamp': datetime.utcnow().isoformat(),
        'method': request.method,
        'path': request.path,
        'remote_addr': request.remote_addr,
        'user_agent': request.user_agent.string,
        'query_params': dict(request.args),
        'headers': dict(request.headers),
    }

    # Include form data for POST requests
    if request.method == 'POST':
        request_data['form_data'] = dict(request.form)

    # Include JSON data if present
    if request.is_json:
        request_data['json_data'] = request.get_json()

    # Log the request data
    logger.info(f"Request logged: {request_data}")

    # Return logged data as JSON (safe from XSS)
    return jsonify(request_data), 200


if __name__ == '__main__':
    app.run(debug=True)
