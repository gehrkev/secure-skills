from flask import Flask, request

app = Flask(__name__)

@app.route('/evaluate')
def evaluate():
    equation = request.args.get('equation')
    try:
        result = eval(equation)
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == '__main__':
    app.run()
