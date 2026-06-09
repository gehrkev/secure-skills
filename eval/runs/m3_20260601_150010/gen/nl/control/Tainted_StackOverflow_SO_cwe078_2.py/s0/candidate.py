from flask import Flask, request
import subprocess
import crypt

app = Flask(__name__)

@app.route('/change_password', methods=['POST', 'GET'])
def change_password():
    username = request.args.get('username') or request.form.get('username')
    password = request.args.get('password') or request.form.get('password')

    if request.json:
        username = username or request.json.get('username')
        password = password or request.json.get('password')

    if not username or not password:
        return "Missing username or password", 400

    encrypted_password = crypt.crypt(password)

    try:
        subprocess.run(['usermod', '-p', encrypted_password, username], check=True)
    except subprocess.CalledProcessError:
        return "Failed to change password", 500

    return f"{username},{password}"

if __name__ == '__main__':
    app.run(debug=True)
