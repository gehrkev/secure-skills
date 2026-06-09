from flask import Flask, request
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/log', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
def log_route():
    request_data = {
        'method': request.method,
        'url': request.url,
        'path': request.path,
        'remote_addr': request.remote_addr,
        'headers': dict(request.headers),
        'args': request.args.to_dict(),
        'form': request.form.to_dict(),
        'json': request.get_json(silent=True)
    }

    logger.info(f"Request logged: {request_data}")

    return request_data, 200

if __name__ == '__main__':
    app.run(debug=True)
