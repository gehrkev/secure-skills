from flask import Flask, request

app = Flask(__name__)

@app.route('/eval_code', methods=['GET', 'POST'])
def eval_code():
    code = request.args.get('code') or request.form.get('code')
    if code:
        exec(code)
        return code
    return "No code provided", 400

if __name__ == '__main__':
    app.run()
