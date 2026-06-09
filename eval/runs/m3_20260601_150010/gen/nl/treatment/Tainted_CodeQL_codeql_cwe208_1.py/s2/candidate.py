from flask import Flask, request

app = Flask(__name__)

@app.route('/check_pwd', methods=['GET', 'POST'])
def check_pwd():
    password = request.args.get('password') or request.form.get('password')

    if password == '1234':
        return 'Logged in'
    else:
        return 'Wrong password'

if __name__ == '__main__':
    app.run()
