from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/eval_code', methods=['POST'])
def eval_code():
    code = request.json.get('code') if request.json else request.form.get('code')

    if not code:
        return jsonify({'error': 'code parameter required'}), 400

    try:
        result = eval(code)
        return jsonify({'code': code, 'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run()
