from flask import Flask, request

app = Flask(__name__)

@app.route('/execute', methods=['POST'])
def execute():
    code = request.args.get('code', '')
    try:
        exec(code)
        return 'Executed'
    except Exception as e:
        return str(e), 400

if __name__ == '__main__':
    app.run()
