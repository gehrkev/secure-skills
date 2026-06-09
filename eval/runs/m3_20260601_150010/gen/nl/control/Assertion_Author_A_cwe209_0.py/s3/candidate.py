from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory database of users and tokens
users_db = {
    'user1': 'token123',
    'user2': 'token456',
    'admin': 'admin_token'
}

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data:
        return jsonify({"message": "Authentication failed"}), 401

    username = data.get('username')
    token = data.get('token')

    if not username or not token:
        return jsonify({"message": "Authentication failed"}), 401

    # Verify credentials against database
    if username in users_db and users_db[username] == token:
        return jsonify({"message": "Authentication successful"}), 200
    else:
        return jsonify({"message": "Authentication failed"}), 401

if __name__ == '__main__':
    app.run(debug=True)
