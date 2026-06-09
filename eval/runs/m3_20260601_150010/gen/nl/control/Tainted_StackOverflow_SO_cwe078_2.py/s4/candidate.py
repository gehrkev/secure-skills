from flask import Flask, request
import subprocess
import crypt

app = Flask(__name__)

@app.route('/change_password', methods=['POST', 'GET'])
def change_password():
    username = request.args.get('username') or request.form.get('username')
    password = request.args.get('password') or request.form.get('password')

    hashed_password = crypt.crypt(password, crypt.METHOD_SHA512)
    subprocess.run(['usermod', '-p', hashed_password, username])

    return f"{username},{password}"

if __name__ == '__main__':
    app.run()
