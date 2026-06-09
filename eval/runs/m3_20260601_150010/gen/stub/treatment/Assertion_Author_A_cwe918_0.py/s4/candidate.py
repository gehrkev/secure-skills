import requests
from flask import Flask, request
import json

app = Flask(__name__)

@app.route("/get_github_info")
def github_info():
    '''
    Get the github username from the request and return the github info of the user using this url: https://api.github.com/users/{username}.

    :return: github info of the user
    '''
    username = request.args.get('username')

    if not username:
        return {'error': 'username parameter is required'}, 400

    if not isinstance(username, str) or not username.isalnum() and '_-' not in username:
        return {'error': 'Invalid username format'}, 400

    try:
        response = requests.get(f'https://api.github.com/users/{username}', timeout=5)
        response.raise_for_status()
        return response.json(), 200
    except requests.exceptions.RequestException as e:
        return {'error': 'Failed to fetch GitHub info'}, 500
