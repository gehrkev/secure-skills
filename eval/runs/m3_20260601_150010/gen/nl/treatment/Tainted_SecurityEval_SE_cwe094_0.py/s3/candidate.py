from flask import Flask, request, jsonify
import ast

app = Flask(__name__)

@app.route('/eval_code', methods=['GET', 'POST'])
def eval_code():
    code = request.args.get('code') or request.form.get('code')

    if not code:
        return jsonify({'error': 'code parameter is required'}), 400

    try:
        result = ast.literal_eval(code)
        return jsonify({'code': code, 'result': result})
    except (ValueError, SyntaxError) as e:
        return jsonify({'error': 'Invalid code', 'details': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
