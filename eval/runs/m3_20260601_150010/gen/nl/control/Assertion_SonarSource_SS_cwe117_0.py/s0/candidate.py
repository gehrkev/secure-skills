from flask import Flask, request, jsonify
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/log', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
def log_route():
    request_data = {
        'method': request.method,
        'path': request.path,
        'remote_addr': request.remote_addr,
        'headers': dict(request.headers),
        'args': dict(request.args),
    }

    if request.is_json:
        request_data['json'] = request.get_json()

    if request.form:
        request_data['form'] = dict(request.form)

    logger.info(f"Incoming request: {request_data}")

    return jsonify(request_data)

if __name__ == '__main__':
    app.run(debug=True)
