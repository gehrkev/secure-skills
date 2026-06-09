from flask import Flask, request, jsonify
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/log', methods=['GET', 'POST'])
def log_request():
    request_data = {
        'method': request.method,
        'path': request.path,
        'remote_addr': request.remote_addr,
        'user_agent': request.headers.get('User-Agent', ''),
        'query_params': dict(request.args),
        'headers': dict(request.headers),
    }

    if request.method == 'POST':
        if request.is_json:
            request_data['json_body'] = request.get_json()
        else:
            request_data['form_data'] = dict(request.form)

    logger.info(f"Request logged: {request_data}")

    return jsonify(request_data)

if __name__ == '__main__':
    app.run(debug=True)
