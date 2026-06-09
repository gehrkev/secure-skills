from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/ping', methods=['GET'])
def ping():
    link = request.args.get('link')

    if not link:
        return jsonify({'error': 'link parameter is required'}), 400

    try:
        response = requests.get(link, timeout=5)
        return jsonify({'link': link, 'status': response.status_code}), 200
    except Exception as e:
        return jsonify({'link': link, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
