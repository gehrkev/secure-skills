from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/evalInput', methods=['GET', 'POST'])
def eval_input():
    input_str = request.args.get('inputStr') or request.form.get('inputStr')

    try:
        result = eval(input_str)
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run()
