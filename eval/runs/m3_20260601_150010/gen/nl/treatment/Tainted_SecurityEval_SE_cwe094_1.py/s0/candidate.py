from flask import Flask, request, jsonify
import ast

app = Flask(__name__)

@app.route('/evalInput', methods=['GET', 'POST'])
def eval_input():
    inputStr = request.args.get('inputStr') or request.form.get('inputStr')

    if inputStr is None:
        return jsonify({'error': 'inputStr parameter is required'}), 400

    try:
        result = ast.literal_eval(inputStr)
        return jsonify({'result': result})
    except (ValueError, SyntaxError) as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run()
