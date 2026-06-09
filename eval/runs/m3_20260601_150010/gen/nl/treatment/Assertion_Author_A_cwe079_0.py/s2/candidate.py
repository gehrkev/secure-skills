from flask import Flask, request

app = Flask(__name__)

@app.route('/first_name')
def greet():
    first_name = request.args.get('first_name', '')
    if first_name:
        return f"Greetings, {first_name}!"
    return "Greetings, !"

if __name__ == '__main__':
    app.run()
