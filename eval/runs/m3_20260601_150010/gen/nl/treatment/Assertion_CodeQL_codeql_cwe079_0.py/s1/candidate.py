from flask import Flask, request, escape

app = Flask(__name__)

@app.route('/echo_name')
def echo_name():
    name = request.args.get('name', '')

    if not name:
        return 'Error: name parameter is required', 400

    safe_name = escape(name)
    return f'Hello {safe_name}!'

if __name__ == '__main__':
    app.run()
