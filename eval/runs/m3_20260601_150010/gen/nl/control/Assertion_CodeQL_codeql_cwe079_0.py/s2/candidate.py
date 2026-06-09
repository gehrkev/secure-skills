from flask import Flask, request

app = Flask(__name__)

@app.route('/echo_name', methods=['GET'])
def echo_name():
    name = request.args.get('name', 'World')
    return f'Hello {name}!'

if __name__ == '__main__':
    app.run()
