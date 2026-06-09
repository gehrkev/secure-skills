from flask import Flask, request

app = Flask(__name__)

@app.route('/eval_code', methods=['GET', 'POST'])
def eval_code():
    code = request.args.get('code', '')
    eval(code)
    return code

if __name__ == '__main__':
    app.run()
