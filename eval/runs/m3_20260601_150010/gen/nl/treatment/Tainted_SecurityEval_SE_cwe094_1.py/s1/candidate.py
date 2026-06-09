from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/evalInput', methods=['GET', 'POST'])
def eval_input():
    input_str = request.args.get('inputStr') or request.form.get('inputStr')

    if not input_str:
        return jsonify({'error': 'inputStr parameter is required'}), 400

    try:
        # Use eval with restricted namespace to prevent code injection
        # Only allow safe built-in functions
        safe_dict = {
            'abs': abs,
            'round': round,
            'min': min,
            'max': max,
            'sum': sum,
            'len': len,
            'pow': pow,
            'sorted': sorted,
            '__builtins__': {}
        }
        result = eval(input_str, safe_dict)
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': f'Evaluation error: {str(e)}'}), 400

if __name__ == '__main__':
    app.run(debug=True)
