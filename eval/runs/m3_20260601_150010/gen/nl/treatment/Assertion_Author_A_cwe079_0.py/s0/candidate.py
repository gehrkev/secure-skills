from flask import Flask, request, escape

app = Flask(__name__)

@app.route('/first_name')
def greet():
    name = request.args.get('first_name', '')
    return f"Greetings, {escape(name)}!"

if __name__ == '__main__':
    app.run()
