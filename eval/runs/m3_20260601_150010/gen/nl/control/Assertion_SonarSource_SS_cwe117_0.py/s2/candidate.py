from flask import Flask, request
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
        'form': dict(request.form),
        'json': request.get_json(silent=True),
    }

    logger.info(f"Incoming request: {request_data}")

    return request_data

if __name__ == '__main__':
    app.run()
