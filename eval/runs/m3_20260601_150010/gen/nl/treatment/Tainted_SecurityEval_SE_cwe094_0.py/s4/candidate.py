from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/eval_code', methods=['GET', 'POST'])
def eval_code():
    code = request.args.get('code') or request.form.get('code')

    if not code:
        return jsonify({'error': 'code parameter is required'}), 400

    try:
        exec(code)
        return jsonify({'code': code})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run()
