from flask import Flask, request
import subprocess
import crypt

app = Flask(__name__)

@app.route('/change_password', methods=['POST'])
def change_password():
    username = request.form.get('username')
    password = request.form.get('password')

    if not username or not password:
        return 'Missing username or password', 400

    try:
        password_hash = crypt.crypt(password, crypt.METHOD_SHA512.ident + crypt.mksalt(crypt.METHOD_SHA512))
        subprocess.run(
            ['usermod', '-p', password_hash, username],
            check=True,
            capture_output=True
        )

        return f'{username},{password}'
    except subprocess.CalledProcessError:
        return 'Failed to change password', 500
    except Exception:
        return 'Error changing password', 500

if __name__ == '__main__':
    app.run()
