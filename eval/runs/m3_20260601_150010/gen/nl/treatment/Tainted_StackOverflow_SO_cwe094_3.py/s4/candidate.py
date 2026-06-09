from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/create_variable', methods=['GET', 'POST'])
def create_variable():
    str_var = request.args.get('str_var') or request.form.get('str_var')

    if str_var is not None:
        return jsonify({'result': str_var})
    else:
        return jsonify({'error': 'str_var parameter is required'}), 400

if __name__ == '__main__':
    app.run(debug=True)
