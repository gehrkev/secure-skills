from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/evalInput')
def eval_input():
    inputStr = request.args.get('inputStr')
    result = eval(inputStr)
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run()
