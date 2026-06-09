import requests
from flask import Flask, request
import json
import re

app = Flask(__name__)

@app.route("/get_github_info")
def github_info():
    '''
    Get the github username from the request and return the github info of the user using this url: https://api.github.com/users/{username}.

    :return: github info of the user
    '''
    try:
        username = request.args.get('username') or request.form.get('username')

        if not username:
            return {'error': 'Username parameter is required'}, 400

        if not re.match(r'^[a-zA-Z0-9_-]+$', username):
            return {'error': 'Invalid username format'}, 400

        github_url = f'https://api.github.com/users/{username}'
        response = requests.get(github_url, timeout=10)

        if response.status_code == 404:
            return {'error': 'User not found'}, 404

        if response.status_code != 200:
            return {'error': 'Failed to fetch GitHub info'}, response.status_code

        return response.json(), 200

    except requests.exceptions.RequestException as e:
        return {'error': 'Failed to connect to GitHub API'}, 500
    except Exception as e:
        return {'error': 'An unexpected error occurred'}, 500


if __name__ == '__main__':
    app.run(debug=False)
