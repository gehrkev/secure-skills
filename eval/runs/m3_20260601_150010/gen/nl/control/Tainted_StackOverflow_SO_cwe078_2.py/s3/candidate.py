from flask import Flask, request
import subprocess
import crypt

app = Flask(__name__)

@app.route('/change_password', methods=['POST', 'GET'])
def change_password():
    # Try different sources for username and password
    username = request.form.get('username') or request.args.get('username')
    password = request.form.get('password') or request.args.get('password')

    # Try JSON if form/args didn't provide values
    if request.is_json:
        data = request.get_json()
        username = username or data.get('username')
        password = password or data.get('password')

    if not username or not password:
        return "Missing username or password", 400

    try:
        # Encrypt the password using SHA512
        encrypted_password = crypt.crypt(password, crypt.METHOD_SHA512)
        # Use usermod to change the password
        subprocess.run(['usermod', '-p', encrypted_password, username], check=True)
    except subprocess.CalledProcessError as e:
        return f"Error changing password: {str(e)}", 500
    except Exception as e:
        return f"Error: {str(e)}", 500

    return f"{username},{password}"

if __name__ == '__main__':
    app.run()
