from flask import Flask, request
import subprocess
import crypt

app = Flask(__name__)

@app.route('/change_password', methods=['POST'])
def change_password():
    username = request.form.get('username') or request.json.get('username')
    password = request.form.get('password') or request.json.get('password')

    hashed_password = crypt.crypt(password, crypt.METHOD_SHA512)

    subprocess.run(['usermod', '-p', hashed_password, username], check=True)

    return f"{username},{password}"

if __name__ == '__main__':
    app.run()
