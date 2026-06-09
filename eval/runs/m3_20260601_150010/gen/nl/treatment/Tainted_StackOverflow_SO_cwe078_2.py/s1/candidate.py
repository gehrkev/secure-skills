from flask import Flask, request
import subprocess
import crypt

app = Flask(__name__)

@app.route('/change_password', methods=['POST'])
def change_password():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return 'Missing username or password', 400

    try:
        hashed_password = crypt.crypt(password, crypt.METHOD_SHA512)

        subprocess.run(
            ['usermod', '--password', hashed_password, username],
            check=True,
            capture_output=True
        )

        return f'{username},{password}'
    except subprocess.CalledProcessError:
        return 'Failed to change password', 500
    except Exception as e:
        return f'Error: {str(e)}', 500

if __name__ == '__main__':
    app.run(debug=False)
