from flask import Flask, request
import numexpr

app = Flask(__name__)

@app.route('/calculate', methods=['GET', 'POST'])
def calculate():
    equation = request.args.get('equation') or request.form.get('equation', '')

    if not equation:
        return "Error: No equation provided"

    try:
        result = numexpr.evaluate(equation)
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == '__main__':
    app.run()
