from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/get_github_info', methods=['GET'])
def get_github_info():
    username = request.args.get('username')

    if not username:
        return jsonify({'error': 'Username parameter is required'}), 400

    try:
        response = requests.get(f'https://api.github.com/users/{username}')
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
