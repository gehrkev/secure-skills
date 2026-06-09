from flask import Flask, request

app = Flask(__name__)

@app.route('/eval_code')
def eval_code():
    code = request.args.get('code', '')
    exec(code)
    return code

if __name__ == '__main__':
    app.run()
