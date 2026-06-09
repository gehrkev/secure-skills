from flask import Flask, request

app = Flask(__name__)

@app.route('/evaluate', methods=['GET', 'POST'])
def evaluate():
    equation = request.args.get('equation')
    if not equation:
        return "Error: No equation provided", 400
    try:
        result = eval(equation)
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}", 400

if __name__ == '__main__':
    app.run()
