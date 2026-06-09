from flask import Flask, request, jsonify
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.route('/log', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
def log():
    request_data = {
        'method': request.method,
        'path': request.path,
        'url': request.url,
        'headers': dict(request.headers),
        'query_params': request.args.to_dict(),
    }

    if request.method in ['POST', 'PUT', 'PATCH']:
        try:
            request_data['json'] = request.get_json()
        except Exception:
            request_data['data'] = request.data.decode('utf-8', errors='ignore')

    logger.info(f"Logged request: {request_data}")

    return jsonify(request_data)


if __name__ == '__main__':
    app.run(debug=True)
