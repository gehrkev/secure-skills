from flask import Flask, request

app = Flask(__name__)

@app.route('/logging')
def logging_route():
    name = request.args.get('name', '')

    if name and name != 'admin':
        app.logger.info(f'Name parameter: {name}')

    return 'OK'
