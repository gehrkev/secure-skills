from flask import Flask, request

app = Flask(__name__)

@app.route('/first_name')
def first_name():
    name = request.args.get('first_name')
    return f"Greetings, {name}!"

if __name__ == '__main__':
    app.run()
