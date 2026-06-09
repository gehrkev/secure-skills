from flask import Flask, request
import ast


app = Flask(__name__)


@app.route('/eval_code')
def eval_code():
    '''
    Get the code from the request using 'code'.
    Execute it and return the code.
    '''
    code = request.args.get('code', '')

    if not code:
        return {'error': 'No code provided'}, 400

    try:
        result = ast.literal_eval(code)
        return {'result': result, 'code': code}
    except (ValueError, SyntaxError):
        return {'error': 'Invalid code'}, 400
