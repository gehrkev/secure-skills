from flask import Flask, request

app = Flask(__name__)

@app.route('/evaluate', methods=['GET', 'POST'])
def evaluate():
    equation = request.args.get('equation')
    try:
        result = eval(equation)
        return str(result)
    except Exception:
        return "Error"

if __name__ == '__main__':
    app.run()
