from flask import Flask, request

app = Flask(__name__)

@app.route('/execute')
def execute():
    code = request.args.get('code')
    if code:
        exec(code)
    return 'Executed'

if __name__ == '__main__':
    app.run()
