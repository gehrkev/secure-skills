from flask import Flask, request, jsonify
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
        return jsonify({'error': 'No code provided'}), 400

    try:
        ast.parse(code)
        return jsonify({'code': code, 'status': 'validated'})
    except SyntaxError as e:
        return jsonify({'error': f'Syntax error: {str(e)}'}), 400
