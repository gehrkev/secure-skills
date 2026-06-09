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
    username = request.args.get('username')

    if not username:
        return {'error': 'Username is required'}, 400

    if not re.match(r'^[a-zA-Z0-9-]{1,39}$', username):
        return {'error': 'Invalid username'}, 400

    try:
        response = requests.get(f'https://api.github.com/users/{username}')
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        return {'error': 'Failed to fetch user data'}, 500
