from flask import Flask, request

app = Flask(__name__)

@app.route('/check_pwd', methods=['GET', 'POST'])
def check_pwd():
    # Get password from query string (GET) or form data/JSON (POST)
    password = request.args.get('password') or request.form.get('password')

    if not password and request.is_json:
        json_data = request.get_json(silent=True)
        if json_data:
            password = json_data.get('password')

    password = password or ''

    if password == '1234':
        return 'Logged in'
    else:
        return 'Wrong password'

if __name__ == '__main__':
    app.run()
