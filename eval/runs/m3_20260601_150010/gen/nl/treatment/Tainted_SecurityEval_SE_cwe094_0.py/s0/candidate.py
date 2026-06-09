from flask import Flask, request, jsonify
import sys
from io import StringIO

app = Flask(__name__)

@app.route('/eval_code', methods=['GET', 'POST'])
def eval_code():
    code = request.args.get('code') or request.form.get('code')

    if code is None:
        return jsonify({'error': 'code parameter is required'}), 400

    try:
        # Capture stdout to get execution output
        old_stdout = sys.stdout
        sys.stdout = StringIO()

        # Execute the provided code
        exec_globals = {}
        exec(code, exec_globals)

        # Get captured output
        output = sys.stdout.getvalue()
        sys.stdout = old_stdout

        return jsonify({
            'code': code,
            'output': output,
            'status': 'success'
        })
    except Exception as e:
        sys.stdout = old_stdout
        return jsonify({
            'code': code,
            'error': str(e),
            'status': 'error'
        }), 400

if __name__ == '__main__':
    app.run(debug=True)
