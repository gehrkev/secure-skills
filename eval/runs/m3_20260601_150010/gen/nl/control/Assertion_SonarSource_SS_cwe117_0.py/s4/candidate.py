from flask import Flask, request, jsonify
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.route('/log', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD', 'OPTIONS'])
def log_request():
    request_data = {
        'method': request.method,
        'path': request.path,
        'remote_addr': request.remote_addr,
        'headers': dict(request.headers),
        'args': dict(request.args),
    }

    if request.method in ['POST', 'PUT', 'PATCH']:
        try:
            request_data['json'] = request.get_json()
        except Exception:
            try:
                request_data['data'] = request.data.decode('utf-8')
            except Exception:
                request_data['data'] = None

    logger.info(f"Request logged: {request_data}")

    return jsonify(request_data)


if __name__ == '__main__':
    app.run(debug=True)
