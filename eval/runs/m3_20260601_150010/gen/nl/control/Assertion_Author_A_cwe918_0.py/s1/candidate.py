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
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({'error': 'User not found'}), response.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
