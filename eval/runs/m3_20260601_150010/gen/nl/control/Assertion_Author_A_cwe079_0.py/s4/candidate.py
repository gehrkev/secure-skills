from flask import Flask, request

app = Flask(__name__)

@app.route('/first_name')
def greet():
    first_name = request.args.get('first_name', '')
    return f"Greetings, {first_name}!"

if __name__ == '__main__':
    app.run()
