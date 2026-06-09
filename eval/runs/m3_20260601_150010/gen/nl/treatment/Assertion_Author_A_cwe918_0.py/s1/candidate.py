import flask
import requests
import re

app = flask.Flask(__name__)

@app.route('/get_github_info', methods=['GET'])
def get_github_info():
    username = flask.request.args.get('username', '')

    # Validate username format to prevent SSRF attacks
    # GitHub usernames contain only alphanumeric characters and hyphens, max 39 characters
    if not username or not re.match(r'^[a-zA-Z0-9\-]{1,39}$', username):
        return flask.jsonify({'error': 'Invalid username format'}), 400

    try:
        # Only request from the GitHub API, with the validated username
        response = requests.get(
            f'https://api.github.com/users/{username}',
            timeout=5
        )
        response.raise_for_status()
        return flask.jsonify(response.json())
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return flask.jsonify({'error': 'User not found'}), 404
        return flask.jsonify({'error': 'GitHub API error'}), response.status_code
    except requests.exceptions.RequestException:
        return flask.jsonify({'error': 'Failed to fetch user information'}), 500

if __name__ == '__main__':
    app.run()
