from flask import Flask, request
import subprocess
import crypt

app = Flask(__name__)

@app.route('/change_password', methods=['POST'])
def change_password():
    if request.is_json:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
    else:
        username = request.form.get('username')
        password = request.form.get('password')

    if not username or not password:
        return "Error: username and password are required", 400

    try:
        # Hash the password using SHA512
        hashed_password = crypt.crypt(password, crypt.METHOD_SHA512)

        # Use usermod to change the password
        subprocess.run(
            ['usermod', '-p', hashed_password, username],
            check=True,
            capture_output=True
        )

        return f"{username},{password}"
    except subprocess.CalledProcessError:
        return "Error: Failed to change password", 500

if __name__ == '__main__':
    app.run(debug=False)
