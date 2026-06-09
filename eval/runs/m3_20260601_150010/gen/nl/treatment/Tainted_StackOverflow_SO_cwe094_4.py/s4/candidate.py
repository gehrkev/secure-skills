import math
from flask import Flask, request

app = Flask(__name__)

@app.route('/evaluate', methods=['GET'])
def evaluate():
    equation = request.args.get('equation')

    if equation is None:
        return 'Error: equation parameter is required', 400

    try:
        safe_dict = {name: getattr(math, name) for name in dir(math) if not name.startswith('_')}
        safe_dict['__builtins__'] = {}
        result = eval(equation, safe_dict)
        return str(result)
    except Exception as e:
        return f'Error: {str(e)}', 400

if __name__ == '__main__':
    app.run()
