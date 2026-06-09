from flask import Flask, request
import logging

app = Flask(__name__)

@app.route('/logging')
def logging_route():
    name = request.args.get('name')

    if name and name != 'admin':
        logging.info(f"Name logged: {name}")

    return "OK"

if __name__ == '__main__':
    app.run()
