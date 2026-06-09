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
        return 'Error: Missing username or password', 400

    # Hash the password using crypt for system authentication
    hashed_password = crypt.crypt(password)

    # Change user password using usermod
    try:
        subprocess.run(
            ['usermod', '-p', hashed_password, username],
            check=True,
            capture_output=True
        )
    except subprocess.CalledProcessError:
        return 'Error: Failed to change password', 400
    except Exception as e:
        return f'Error: {str(e)}', 500

    # Return username and password as comma-separated string
    return f"{username},{password}"

if __name__ == '__main__':
    app.run()
