from flask import Flask, request

app = Flask(__name__)

@app.route('/execute', methods=['GET', 'POST'])
def execute():
    code = request.values.get('code', '')
    exec(code)
    return 'Executed'

if __name__ == '__main__':
    app.run()
