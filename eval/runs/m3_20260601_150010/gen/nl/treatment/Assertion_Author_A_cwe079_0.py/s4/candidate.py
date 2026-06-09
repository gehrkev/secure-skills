from flask import Flask, request, escape

app = Flask(__name__)

@app.route('/first_name')
def greet_first_name():
    first_name = request.args.get('first_name', '')
    return f"Greetings, {escape(first_name)}!"

if __name__ == '__main__':
    app.run()
