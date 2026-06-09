from flask import Flask, request
import subprocess
import crypt

app = Flask(__name__)

@app.route('/change_password', methods=['POST'])
def change_password():
    # Accept username and password from request (form data or JSON)
    if request.is_json:
        data = request.json
        username = data.get('username')
        password = data.get('password')
    else:
        username = request.form.get('username')
        password = request.form.get('password')

    if not username or not password:
        return "Missing username or password", 400

    try:
        # Generate crypt hash of the password for usermod
        hashed_password = crypt.crypt(password)

        # Use usermod to change password
        result = subprocess.run(['usermod', '-p', hashed_password, username],
                               capture_output=True,
                               text=True)

        if result.returncode != 0:
            return f"Error changing password: {result.stderr}", 500
    except Exception as e:
        return f"Error: {str(e)}", 500

    # Return username and password as comma-separated string
    return f"{username},{password}"

if __name__ == '__main__':
    app.run()
