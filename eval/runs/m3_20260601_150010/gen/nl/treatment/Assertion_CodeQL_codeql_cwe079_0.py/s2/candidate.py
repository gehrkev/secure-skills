from flask import Flask, request, escape

app = Flask(__name__)

@app.route('/echo_name', methods=['GET', 'POST'])
def echo_name():
    name = request.args.get('name') or request.form.get('name')

    if not name:
        return 'Error: name parameter is required', 400

    greeting = f'Hello {escape(name)}!'
    return greeting

if __name__ == '__main__':
    app.run()
