from flask import Flask, request
import subprocess

app = Flask(__name__)

@app.route('/change_password', methods=['POST'])
def change_password():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return {'error': 'Missing username or password'}, 400

    try:
        process = subprocess.Popen(['chpasswd'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate(input=f'{username}:{password}\n')

        if process.returncode != 0:
            return {'error': 'Failed to change password'}, 500

        return f'{username},{password}'
    except Exception as e:
        return {'error': str(e)}, 500

if __name__ == '__main__':
    app.run()
